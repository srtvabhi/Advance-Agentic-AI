import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


DOCUMENTS = [
    "Remote work is allowed up to two days per week for hybrid eligible roles.",
    "Three remote days per week requires manager approval and business justification.",
    "Employees must use company devices and VPN when working with confidential data.",
]


# Load only this folder's .env file and create an OpenAI SDK client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Function: create an embedding for ChromaDB search.
def embed(client: OpenAI, text: str) -> list[float]:
    response = client.embeddings.create(model=os.environ["Embedding_Model"], input=text)
    return response.data[0].embedding


# Function: build an in-memory Chroma collection.
def build_collection(client: OpenAI):
    chroma = chromadb.Client()
    collection = chroma.get_or_create_collection("crash_course_rag")
    collection.add(
        ids=[f"doc-{index}" for index, _ in enumerate(DOCUMENTS)],
        documents=DOCUMENTS,
        embeddings=[embed(client, text) for text in DOCUMENTS],
    )
    return collection


# Function: retrieve context and ask the model for a grounded answer.
def ask_rag_agent(client: OpenAI, question: str) -> str:
    collection = build_collection(client)
    results = collection.query(query_embeddings=[embed(client, question)], n_results=2)
    context = "\n".join(results["documents"][0])
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer only from the provided context."},
            {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
        ],
    )
    return response.choices[0].message.content or ""


# Run the ChromaDB-backed single RAG agent.
def main() -> None:
    client = create_client()
    question = input("Ask policy question: ").strip() or "Can I work remotely three days per week?"
    print("\nAgent:", ask_rag_agent(client, question))


if __name__ == "__main__":
    main()

