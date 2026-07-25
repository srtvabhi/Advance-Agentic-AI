from langsmith import traceable

from config.settings import configure_langsmith, create_agents_run_config, create_openai_client
from lab_agents.rag_agent import create_retrieval_plan, generate_grounded_answer, select_data_domain
from services.document_loader_service import load_enterprise_documents
from services.observability_service import (
    estimate_tokens,
    evaluate_rag_response,
    format_observability_report,
    summarize_retrieved_chunks,
    timed_step,
)
from services.vector_store_service import has_existing_index, index_chunks, semantic_search


# This service is the main orchestration layer for Lab 20.
# It connects agentic RAG with LangSmith observability. The workflow traces
# domain routing, planning, vector retrieval, answer generation, and evaluation.


INDEX_READY = False


# Function: build the ChromaDB indexes from HR, Sales, and Marketing data.
# Logic:
# 1. Load HR PDFs, Sales CSV rows, and Marketing campaign notes.
# 2. Convert each source into searchable chunks.
# 3. Store each domain in its own ChromaDB vector-store folder.
@traceable(
    name="build_or_reuse_vector_indexes",
    run_type="chain",
    process_inputs=lambda _: {"operation": "build or reuse HR, Sales, and Marketing vector stores"},
)
def build_index(openai_client) -> None:
    global INDEX_READY

    if INDEX_READY:
        return

    if has_existing_index():
        print("Using existing HR, Sales, and Marketing vector stores. Skipping index build.")
        INDEX_READY = True
        return

    chunks = load_enterprise_documents()
    index_chunks(openai_client, chunks)
    INDEX_READY = True


# Function: run the full Agentic RAG workflow for one user question.
# Logic:
# 1. Create the Azure OpenAI client.
# 2. Build or reuse the separate vector indexes.
# 3. Ask the model to select the best data domain.
# 4. Ask the model to create a retrieval plan for that domain.
# 5. Search only the selected vector store, or all vector stores when domain is All.
# 6. Generate a grounded answer using only retrieved context.
# 7. Return the domain, plan, answer, and citations as one formatted string.
@traceable(name="lab20_agentic_rag_observability_workflow", run_type="chain")
def run_agentic_rag(question: str) -> str:
    configure_langsmith()
    metrics = []
    client = create_openai_client()
    _, metric = timed_step("build_or_reuse_vector_indexes", lambda: build_index(client))
    metrics.append(metric)

    selected_domain, metric = timed_step(
        "domain_router_agent",
        lambda: select_data_domain(
            question,
            create_agents_run_config("Lab 20 - Domain Routing"),
        ),
    )
    metrics.append(metric)

    plan, metric = timed_step(
        "retrieval_planner_agent",
        lambda: create_retrieval_plan(
            question,
            selected_domain,
            create_agents_run_config("Lab 20 - Retrieval Planning"),
        ),
    )
    metrics.append(metric)

    retrieved_chunks, metric = timed_step(
        "separate_vector_store_retrieval",
        lambda: traced_vector_retrieval(client, question, selected_domain, top_k=4),
    )
    metrics.append(metric)

    answer, metric = timed_step(
        "grounded_answer_agent",
        lambda: generate_grounded_answer(
            question,
            selected_domain,
            plan,
            retrieved_chunks,
            create_agents_run_config("Lab 20 - Grounded Answer"),
        ),
    )
    metrics.append(metric)

    evaluation, metric = timed_step(
        "rag_quality_evaluation",
        lambda: evaluate_rag_response(question, selected_domain, retrieved_chunks, answer),
    )
    metrics.append(metric)

    retrieved_summary = summarize_retrieved_chunks(retrieved_chunks)
    estimated_tokens = {
        "question": estimate_tokens(question),
        "retrieval_plan": estimate_tokens(plan),
        "retrieved_context": estimate_tokens("\n".join(chunk.text for chunk in retrieved_chunks)),
        "final_answer": estimate_tokens(answer),
    }
    observability_report = format_observability_report(
        metrics,
        estimated_tokens,
        retrieved_summary,
        evaluation,
    )

    citations = "\n".join(f"- {chunk.citation()}" for chunk in retrieved_chunks)
    return (
        f"--- Selected Data Domain ---\n{selected_domain}\n\n"
        f"--- Retrieval Plan ---\n{plan}\n\n"
        f"--- Answer ---\n{answer}\n\n"
        f"--- Retrieved Citations ---\n{citations}\n\n"
        f"{observability_report}"
    )


def vector_retrieval_trace_inputs(inputs):
    return {
        "question": inputs["question"],
        "selected_domain": inputs["selected_domain"],
        "top_k": inputs["top_k"],
    }


def vector_retrieval_trace_outputs(outputs):
    return summarize_retrieved_chunks(outputs)


@traceable(
    name="separate_vector_store_retrieval",
    run_type="retriever",
    process_inputs=vector_retrieval_trace_inputs,
    process_outputs=vector_retrieval_trace_outputs,
)
def traced_vector_retrieval(openai_client, question: str, selected_domain: str, top_k: int):
    return semantic_search(openai_client, question, category_filter=selected_domain, top_k=top_k)
