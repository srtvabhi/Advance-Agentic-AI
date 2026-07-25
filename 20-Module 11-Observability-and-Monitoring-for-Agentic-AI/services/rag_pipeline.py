from langsmith import traceable

from config.settings import configure_langsmith
from graph.rag_observability_graph import build_rag_observability_graph


# Pipeline entry point:
# Configure LangSmith and invoke the LangGraph workflow for one user question.
@traceable(name="lab20_agentic_rag_observability_workflow", run_type="chain")
def run_agentic_rag(question: str) -> str:
    configure_langsmith()
    workflow = build_rag_observability_graph()
    result = workflow.invoke({"question": question, "metrics": []})
    return result["final_output"]
