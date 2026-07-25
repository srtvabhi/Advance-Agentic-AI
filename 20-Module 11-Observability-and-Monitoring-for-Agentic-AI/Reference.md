# Lab 20 Reference

This reference explains the LangGraph, Azure OpenAI, and LangSmith observability code used in Lab 20.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
python main.py
```

## Environment Variables

The lab loads `.env` from this lab folder only.

```env
AZURE_OPENAI_ENDPOINT=https://kyndrl77777777.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2025-08-07
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
Embedding_Model=text-embedding-3-large
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=lab20_abhishek
```

## LangSmith Configuration

File:

```text
config/settings.py
```

Function:

```python
def configure_langsmith() -> None:
    load_environment()
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ.setdefault("LANGSMITH_PROJECT", "lab20_abhishek")
```

This function enables tracing before LangGraph runs.

## LangChain Azure OpenAI Model

Function:

```python
def create_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=get_required_setting("AZURE_OPENAI_DEPLOYMENT"),
        base_url=get_required_setting("AZURE_OPENAI_ENDPOINT"),
        api_key=get_required_setting("AZURE_OPENAI_API_KEY"),
    )
```

This is the important change for token tracking. The lab uses LangChain `ChatOpenAI` with the Azure OpenAI `/openai/v1` endpoint. LangSmith can show token usage on these LLM spans.

## LangGraph Syntax

File:

```text
graph/rag_observability_graph.py
```

Graph creation:

```python
graph = StateGraph(RAGObservabilityState)
graph.add_node("domain_router_agent", domain_router_node)
graph.add_node("retrieval_planner_agent", retrieval_planner_node)
graph.add_edge(START, "build_or_reuse_vector_indexes")
graph.add_edge("domain_router_agent", "retrieval_planner_agent")
workflow = graph.compile()
```

Each node receives the shared state and returns updates.

```python
def domain_router_node(state: RAGObservabilityState) -> dict:
    selected_domain = select_data_domain(state["question"])
    return {"selected_domain": selected_domain}
```

## Main Workflow Trace

File:

```text
services/rag_pipeline.py
```

Function:

```python
@traceable(name="lab20_agentic_rag_observability_workflow", run_type="chain")
def run_agentic_rag(question: str) -> str:
    configure_langsmith()
    workflow = build_rag_observability_graph()
    result = workflow.invoke({"question": question, "metrics": []})
    return result["final_output"]
```

This creates the parent LangSmith trace and invokes the LangGraph workflow.

## Agent Helper Functions

File:

```text
lab_agents/rag_agent.py
```

The helper functions are:

```python
select_data_domain()
create_retrieval_plan()
generate_grounded_answer()
```

Each helper calls:

```python
ChatOpenAI.invoke()
```

Because these are LangChain model calls, LangSmith can show automatic LLM usage metadata, including token usage when returned by the provider.

## Traceable Syntax

```python
from langsmith import traceable


@traceable(name="domain_router_agent", run_type="chain")
def select_data_domain(question: str) -> str:
    ...
```

The decorator creates a named span in LangSmith. The nested `ChatOpenAI` call creates an LLM span inside it.

## Vector Retrieval Tracing

Function:

```python
@traceable(name="separate_vector_store_retrieval", run_type="retriever")
def traced_vector_retrieval(question, selected_domain, top_k, openai_client):
    return semantic_search(openai_client, question, category_filter=selected_domain, top_k=top_k)
```

The retriever span shows:

- question
- selected domain
- top_k
- source
- page
- category
- distance

## Latency Monitoring

LangSmith automatically shows span duration in the trace waterfall.

The lab also prints local timing with:

```python
def timed_step(step_name: str, action):
    start = perf_counter()
    result = action()
    latency_ms = round((perf_counter() - start) * 1000, 2)
    return result, {"step": step_name, "latency_ms": latency_ms}
```

## Token Monitoring

There are two token views:

| Token View | Where To See It | Meaning |
|---|---|---|
| Automatic LLM token usage | LangSmith nested `ChatOpenAI` LLM spans | Provider/model token metadata captured by LangSmith. |
| Estimated text tokens | `token_usage_estimation` span | Simple learner-friendly estimate for question, retrieved context, plan, and final answer. |

The estimated span uses:

```python
@traceable(name="token_usage_estimation", run_type="chain")
def estimate_rag_token_usage(question, retrieval_plan, retrieved_context, final_answer):
    return {
        "question": estimate_tokens(question),
        "retrieval_plan": estimate_tokens(retrieval_plan),
        "retrieved_context": estimate_tokens(retrieved_context),
        "final_answer": estimate_tokens(final_answer),
        "total_estimated_tokens": ...,
    }
```

## RAG Quality Evaluation

```python
@traceable(name="rag_quality_evaluation", run_type="chain")
def evaluate_rag_response(question, selected_domain, retrieved_chunks, answer):
    ...
```

This produces:

- `citation_score`
- `groundedness_score`
- `relevance_score`
- `overall_score`
- `passed`

## What To Check In LangSmith

Open project:

```text
lab20_abhishek
```

Check:

1. Parent trace: `lab20_agentic_rag_observability_workflow`
2. LangGraph node spans such as `domain_router_agent`, `retrieval_planner_agent`, and `grounded_answer_agent`
3. Nested `ChatOpenAI` spans for automatic token usage
4. Retriever span: `separate_vector_store_retrieval`
5. Estimated text-token span: `token_usage_estimation`
6. Evaluation span: `rag_quality_evaluation`
7. Span durations in the waterfall view

## Useful Prompts

```text
Which sales region has the highest pipeline risk, and what action should the business take next?
```

```text
What is the employee travel reimbursement rule for hotel stays?
```

```text
Summarize the active marketing campaigns and recommend which audience should be prioritized.
```

```text
Compare travel policy considerations with campaign planning risks.
```

```text
Which business area has the clearest operational risk based on the available documents?
```
