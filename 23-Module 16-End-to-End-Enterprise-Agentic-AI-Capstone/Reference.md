# Lab 23 Reference

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Local development uses `.env`:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/openai/v1
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_API_VERSION=2025-08-07
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
Embedding_Model=text-embedding-3-large
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=lab23_capstone
```

Streamlit Community Cloud uses app secrets instead of `.env`.

## Streamlit UI Syntax

```python
import streamlit as st

st.title("Lab 23: End-to-End Enterprise Agentic AI Capstone")
question = st.text_area("Business question")

if st.button("Run Capstone Workflow"):
    answer = run_agentic_rag(question)
    st.markdown(answer)
```

Example from this lab:

```python
def run_question(question: str) -> None:
    with st.spinner("Running enterprise agentic workflow..."):
        answer = run_agentic_rag(question)
    st.session_state.history.append({"question": question, "answer": answer})
```

This creates a simple UI workflow:

- User enters a question.
- Streamlit calls the agentic RAG pipeline.
- The result is saved in session history.

## Streamlit Secrets Syntax

```python
if st.secrets:
    apply_streamlit_secrets(dict(st.secrets))
```

Example from this lab:

```python
def configure_runtime_from_streamlit() -> None:
    if st.secrets:
        apply_streamlit_secrets(dict(st.secrets))
    configure_langsmith()
```

This lets the same app run locally with `.env` and in Streamlit Cloud with app secrets.

## LangGraph Workflow Syntax

```python
workflow = build_rag_observability_graph()
result = workflow.invoke({"question": question, "metrics": []})
```

The graph contains these major nodes:

```text
build_index_node
domain_router_node
retrieval_planner_node
retrieval_node
answer_node
token_usage_node
evaluation_node
final_output_node
```

Each node handles one part of the enterprise workflow.

## Agent Syntax

The LLM calls are implemented through LangChain `ChatOpenAI` using the Azure OpenAI compatible endpoint.

```python
response = model.invoke(
    [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
)
```

The agent functions are:

```text
select_data_domain()
create_retrieval_plan()
generate_grounded_answer()
```

## Vector Store Syntax

ChromaDB stores embeddings locally:

```python
collection = client.get_or_create_collection(name="sales_knowledge")
collection.query(query_embeddings=[embedding], n_results=4)
```

This lab creates separate vector stores for:

```text
HR
Sales
Marketing
```

## Observability Syntax

LangSmith tracing uses:

```python
from langsmith import traceable

@traceable(name="lab23_enterprise_agentic_ai_capstone_workflow", run_type="chain")
def run_agentic_rag(question: str) -> str:
    ...
```

The app also prints:

- latency by step
- estimated token usage
- retrieved evidence
- RAG quality evaluation

## Streamlit Community Cloud Deployment

1. Push the lab to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select the repo and branch.
5. Set the app file to:

```text
app.py
```

6. Add secrets using Streamlit's secrets editor.

Use `.streamlit/secrets.example.toml` as the format reference.

## Useful Commands

Run Streamlit:

```powershell
streamlit run app.py
```

Run terminal version:

```powershell
python main.py
```

Compile Python files:

```powershell
Get-ChildItem -Recurse -Filter *.py | ForEach-Object { python -m py_compile $_.FullName }
```

Check Git:

```powershell
git status
```
