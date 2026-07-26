import os
import sys
from pathlib import Path

import streamlit as st

from config.settings import apply_streamlit_secrets, configure_langsmith
from services.rag_pipeline import run_agentic_rag


DEFAULT_QUESTION = (
    "Which sales region has the highest pipeline risk, and what action should the business take next?"
)

SAMPLE_QUESTIONS = [
    "Which sales region has the highest pipeline risk, and what action should the business take next?",
    "What HR policy should guide an employee relocation request?",
    "Which marketing campaign needs executive attention and why?",
    "Compare sales pipeline risk with current marketing campaign risk.",
    "Create an executive summary using the most relevant enterprise knowledge.",
]


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# Load Streamlit Cloud secrets into environment variables without writing them to disk.
def configure_runtime_from_streamlit() -> None:
    local_secrets_file = Path(".streamlit") / "secrets.toml"
    user_secrets_file = Path.home() / ".streamlit" / "secrets.toml"

    # Streamlit raises an error if st.secrets is read when no secrets file exists.
    # Locally, this lab can run from .env; on Streamlit Cloud, secrets are provided by the platform.
    if local_secrets_file.exists() or user_secrets_file.exists() or os.environ.get("STREAMLIT_RUNTIME"):
        apply_streamlit_secrets(dict(st.secrets))
    configure_langsmith()


# Render reusable setup and deployment guidance in the sidebar.
def render_sidebar() -> None:
    st.sidebar.header("Capstone Runtime")
    st.sidebar.write("Azure OpenAI deployment:", os.environ.get("AZURE_OPENAI_DEPLOYMENT", "not loaded"))
    st.sidebar.write("LangSmith project:", os.environ.get("LANGSMITH_PROJECT", "not loaded"))

    st.sidebar.header("What This App Shows")
    st.sidebar.markdown(
        "- Domain routing across HR, Sales, and Marketing data\n"
        "- Retrieval planning\n"
        "- Separate Chroma vector-store retrieval\n"
        "- Grounded answer generation\n"
        "- Observability summary and quality evaluation"
    )


# Run the capstone workflow and store the result in Streamlit session memory.
def run_question(question: str) -> None:
    with st.spinner("Running enterprise agentic workflow..."):
        full_output = run_agentic_rag(question)
        answer = extract_business_answer(full_output)
    st.session_state.history.append({"question": question, "answer": answer})


# Extract only the business answer for Streamlit users.
# The terminal app still prints the full workflow output with observability metrics.
def extract_business_answer(full_output: str) -> str:
    answer_marker = "--- Answer ---"
    citations_marker = "--- Retrieved Citations ---"

    if answer_marker not in full_output:
        return full_output.strip()

    answer_text = full_output.split(answer_marker, 1)[1]
    if citations_marker in answer_text:
        answer_text = answer_text.split(citations_marker, 1)[0]

    return answer_text.strip()


# Streamlit entry point for the capstone UI.
def main() -> None:
    st.set_page_config(
        page_title="Lab 23 Enterprise Agentic AI Capstone",
        page_icon="AI",
        layout="wide",
    )
    configure_runtime_from_streamlit()
    render_sidebar()

    if "history" not in st.session_state:
        st.session_state.history = []

    st.title("Lab 23: End-to-End Enterprise Agentic AI Capstone")
    st.caption("Streamlit UI for an end-to-end enterprise agentic RAG capstone workflow.")

    question = st.text_area(
        "Business question",
        value=DEFAULT_QUESTION,
        height=100,
        help="Ask a question across HR, Sales, or Marketing enterprise knowledge.",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        run_clicked = st.button("Run Capstone Workflow", type="primary")
    with col2:
        if st.button("Clear Session History"):
            st.session_state.history = []
            st.rerun()

    with st.expander("Sample business prompts"):
        for item in SAMPLE_QUESTIONS:
            st.markdown(f"- {item}")

    if run_clicked:
        cleaned_question = question.strip() or DEFAULT_QUESTION
        run_question(cleaned_question)

    if st.session_state.history:
        st.divider()
        st.subheader("Workflow Results")
        for index, item in enumerate(reversed(st.session_state.history), start=1):
            with st.container(border=True):
                st.markdown(f"**Run {len(st.session_state.history) - index + 1}**")
                st.markdown(f"**Question:** {item['question']}")
                st.markdown(item["answer"])


if __name__ == "__main__":
    main()
