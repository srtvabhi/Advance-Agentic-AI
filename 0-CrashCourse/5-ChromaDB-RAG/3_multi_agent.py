import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


DOCUMENTS = [
    "Severity 1 incidents include confirmed data exfiltration and ransomware.",
    "Severity 2 incidents include suspicious privileged access or likely data exposure.",
    "Evidence must include alert details, cloud audit logs, identity records, and analyst notes.",
]


# Load only this folder's .env file and create an OpenAI SDK client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Function: create an embedding for ChromaDB search.
def embed(client: OpenAI, text: str) -> list[float]:
    response = client.embeddings.create(model=os.environ["Embedding_Model"], input=text)
    return response.data[0].embedding


# Agent 1: retrieval agent gets the most relevant context.
def retriever_agent(client: OpenAI, question: str) -> str:
    chroma = chromadb.Client()
    collection = chroma.get_or_create_collection("crash_course_multi_rag")
    collection.add(ids=[f"doc-{i}" for i, _ in enumerate(DOCUMENTS)], documents=DOCUMENTS, embeddings=[embed(client, text) for text in DOCUMENTS])
    results = collection.query(query_embeddings=[embed(client, question)], n_results=2)
    return "\n".join(results["documents"][0])


# Agent 2: answer agent writes the response from retrieved context.
def answer_agent(client: OpenAI, question: str, context: str) -> str:
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer only from retrieved incident response context."},
            {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
        ],
    )
    return response.choices[0].message.content or ""


# Agent 3: reviewer agent checks if the answer is grounded.
def reviewer_agent(client: OpenAI, answer: str) -> str:
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Review whether the answer is grounded and mention missing evidence."},
            {"role": "user", "content": answer},
        ],
    )
    return response.choices[0].message.content or ""


# Coordinate retrieval, answer, and review agents.
def main() -> None:
    client = create_client()
    question = input("Ask incident question: ").strip() or "How should suspicious privileged access be classified?"
    context = retriever_agent(client, question)
    answer = answer_agent(client, question, context)
    review = reviewer_agent(client, answer)

    print("\n--- Retriever Context ---\n", context)
    print("\n--- Answer Agent ---\n", answer)
    print("\n--- Reviewer Agent ---\n", review)


if __name__ == "__main__":
    main()

