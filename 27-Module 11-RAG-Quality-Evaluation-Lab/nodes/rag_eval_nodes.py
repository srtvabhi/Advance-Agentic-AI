from langsmith import traceable

from models.rag_eval_models import RAGEvaluationState
from services.llm_service import ask_model
from services.retrieval_service import retrieve_context


@traceable(name="retrieve_context_node", run_type="retriever")
def retrieve_context_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Retrieves policy context for the user's question.
    state["retrieved_context"] = retrieve_context(state["question"])
    return state


@traceable(name="generate_answer_node", run_type="chain")
def generate_answer_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Generates a RAG answer grounded in retrieved context.
    state["answer"] = ask_model(
        "You are an HR policy assistant. Answer only from the provided context. If context is insufficient, say what is missing.",
        f"Question: {state['question']}\n\nContext:\n{state['retrieved_context']}",
    )
    return state


@traceable(name="llm_as_judge_node", run_type="chain")
def llm_as_judge_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Evaluates answer quality using an LLM-as-a-judge prompt.
    state["evaluation"] = ask_model(
        "You are a strict RAG evaluator.",
        (
            "Evaluate the answer against the retrieved context. Score each item from 1 to 5: "
            "groundedness, relevance, completeness, and safety. Then give one improvement suggestion.\n\n"
            f"Question: {state['question']}\n\n"
            f"Retrieved context:\n{state['retrieved_context']}\n\n"
            f"Answer:\n{state['answer']}"
        ),
    )
    return state


@traceable(name="observability_report_node", run_type="chain")
def observability_report_node(state: RAGEvaluationState) -> RAGEvaluationState:
    # Creates a practical observability report for participants.
    state["observability_report"] = (
        "RAG observability report:\n"
        "1. Retrieval step captured the context used by the answer.\n"
        "2. Generation step captured the final answer.\n"
        "3. Evaluation step scored groundedness, relevance, completeness, and safety.\n"
        "4. In LangSmith, students can inspect each step as a trace when LANGSMITH_TRACING=true."
    )
    return state
