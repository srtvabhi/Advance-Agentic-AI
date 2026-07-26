from langgraph.graph import END, START, StateGraph
from langsmith import traceable

from config.settings import create_openai_client
from lab_agents.rag_agent import create_retrieval_plan, generate_grounded_answer, select_data_domain
from models.rag_models import RAGObservabilityState
from services.document_loader_service import load_enterprise_documents
from services.observability_service import (
    estimate_rag_token_usage,
    evaluate_rag_response,
    format_observability_report,
    summarize_retrieved_chunks,
    timed_step,
)
from services.vector_store_service import has_existing_index, index_chunks, semantic_search


INDEX_READY = False


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


# LangGraph node:
# Build or reuse HR, Sales, and Marketing vector stores before any retrieval.
def build_index_node(state: RAGObservabilityState) -> dict:
    client = create_openai_client()
    _, metric = timed_step("build_or_reuse_vector_indexes", lambda: build_index(client))
    return {"metrics": [*state.get("metrics", []), metric]}


# LangGraph node:
# Route the question to HR, Sales, Marketing, or All.
def domain_router_node(state: RAGObservabilityState) -> dict:
    selected_domain, metric = timed_step(
        "domain_router_agent",
        lambda: select_data_domain(state["question"]),
    )
    return {
        "selected_domain": selected_domain,
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Create a retrieval plan after the domain is selected.
def retrieval_planner_node(state: RAGObservabilityState) -> dict:
    plan, metric = timed_step(
        "retrieval_planner_agent",
        lambda: create_retrieval_plan(state["question"], state["selected_domain"]),
    )
    return {
        "retrieval_plan": plan,
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Search the selected vector store and trace retrieved evidence.
def retrieval_node(state: RAGObservabilityState) -> dict:
    client = create_openai_client()
    retrieved_chunks, metric = timed_step(
        "separate_vector_store_retrieval",
        lambda: traced_vector_retrieval(
            state["question"],
            state["selected_domain"],
            top_k=4,
            openai_client=client,
        ),
    )
    return {
        "retrieved_chunks": retrieved_chunks,
        "retrieved_summary": summarize_retrieved_chunks(retrieved_chunks),
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Generate a grounded answer from retrieved context.
def answer_node(state: RAGObservabilityState) -> dict:
    answer, metric = timed_step(
        "grounded_answer_agent",
        lambda: generate_grounded_answer(
            state["question"],
            state["selected_domain"],
            state["retrieval_plan"],
            state["retrieved_chunks"],
        ),
    )
    return {
        "answer": answer,
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Estimate token usage as a traceable learner metric.
def token_usage_node(state: RAGObservabilityState) -> dict:
    retrieved_context = "\n".join(chunk.text for chunk in state["retrieved_chunks"])
    estimated_tokens, metric = timed_step(
        "token_usage_estimation",
        lambda: estimate_rag_token_usage(
            state["question"],
            state["retrieval_plan"],
            retrieved_context,
            state["answer"],
        ),
    )
    return {
        "estimated_tokens": estimated_tokens,
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Evaluate whether the RAG answer appears grounded and relevant.
def evaluation_node(state: RAGObservabilityState) -> dict:
    evaluation, metric = timed_step(
        "rag_quality_evaluation",
        lambda: evaluate_rag_response(
            state["question"],
            state["selected_domain"],
            state["retrieved_chunks"],
            state["answer"],
        ),
    )
    return {
        "evaluation": evaluation,
        "metrics": [*state.get("metrics", []), metric],
    }


# LangGraph node:
# Format the final learner output with answer, citations, and observability data.
def final_output_node(state: RAGObservabilityState) -> dict:
    citations = "\n".join(f"- {chunk.citation()}" for chunk in state["retrieved_chunks"])
    observability_report = format_observability_report(
        state["metrics"],
        state["estimated_tokens"],
        state["retrieved_summary"],
        state["evaluation"],
    )
    final_output = (
        f"--- Selected Data Domain ---\n{state['selected_domain']}\n\n"
        f"--- Retrieval Plan ---\n{state['retrieval_plan']}\n\n"
        f"--- Answer ---\n{state['answer']}\n\n"
        f"--- Retrieved Citations ---\n{citations}\n\n"
        f"{observability_report}"
    )
    return {"final_output": final_output}


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
def traced_vector_retrieval(question: str, selected_domain: str, top_k: int, openai_client):
    return semantic_search(openai_client, question, category_filter=selected_domain, top_k=top_k)


def build_rag_observability_graph():
    graph = StateGraph(RAGObservabilityState)
    graph.add_node("build_or_reuse_vector_indexes", build_index_node)
    graph.add_node("domain_router_agent", domain_router_node)
    graph.add_node("retrieval_planner_agent", retrieval_planner_node)
    graph.add_node("separate_vector_store_retrieval", retrieval_node)
    graph.add_node("grounded_answer_agent", answer_node)
    graph.add_node("token_usage_estimation", token_usage_node)
    graph.add_node("rag_quality_evaluation", evaluation_node)
    graph.add_node("format_final_output", final_output_node)

    graph.add_edge(START, "build_or_reuse_vector_indexes")
    graph.add_edge("build_or_reuse_vector_indexes", "domain_router_agent")
    graph.add_edge("domain_router_agent", "retrieval_planner_agent")
    graph.add_edge("retrieval_planner_agent", "separate_vector_store_retrieval")
    graph.add_edge("separate_vector_store_retrieval", "grounded_answer_agent")
    graph.add_edge("grounded_answer_agent", "token_usage_estimation")
    graph.add_edge("token_usage_estimation", "rag_quality_evaluation")
    graph.add_edge("rag_quality_evaluation", "format_final_output")
    graph.add_edge("format_final_output", END)
    return graph.compile()
