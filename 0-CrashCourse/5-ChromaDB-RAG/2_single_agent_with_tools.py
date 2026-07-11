import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


OPENWEATHER_API_KEY = "f256b7a6330c4a019a98db18776ec516"
DOCUMENTS = [
    "Expense reports must be submitted within ten business days after travel.",
    "Receipts are required for any single expense above 25 USD.",
    "Business class requires director and finance approval for international flights over eight hours.",
]


# Load only this folder's .env file and create an OpenAI SDK client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Tool: calculate simple arithmetic expressions safely.
def calculator(expression: str) -> str:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return "Invalid expression."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as exc:
        return f"Calculation error: {exc}"


# Tool: call OpenWeatherMap and return current weather for a city.
def get_weather(city: str) -> str:
    params = urlencode({"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"})
    try:
        with urlopen(f"https://api.openweathermap.org/data/2.5/weather?{params}", timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return f"{data['name']}: {data['weather'][0]['description']}, {data['main']['temp']} C."
    except Exception as exc:
        return f"Weather API error: {exc}"


# Function: create an embedding for ChromaDB search.
def embed(client: OpenAI, text: str) -> list[float]:
    response = client.embeddings.create(model=os.environ["Embedding_Model"], input=text)
    return response.data[0].embedding


# Function: retrieve policy context from ChromaDB.
def retrieve_policy(client: OpenAI, question: str) -> str:
    chroma = chromadb.Client()
    collection = chroma.get_or_create_collection("crash_course_tool_rag")
    collection.add(ids=[f"doc-{i}" for i, _ in enumerate(DOCUMENTS)], documents=DOCUMENTS, embeddings=[embed(client, text) for text in DOCUMENTS])
    results = collection.query(query_embeddings=[embed(client, question)], n_results=2)
    return "\n".join(results["documents"][0])


# Function: combine RAG context with calculator/weather tool result.
def ask_agent(client: OpenAI, question: str) -> str:
    tool_result = "No tool needed."
    lowered = question.lower()
    if "weather" in lowered:
        tool_result = get_weather(question.split(" in ")[-1].strip(" ?.") if " in " in lowered else "Delhi")
    elif "calculate" in lowered:
        tool_result = calculator(lowered.replace("calculate", "").strip())

    context = retrieve_policy(client, question)
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer using policy context and tool result."},
            {"role": "user", "content": f"Question: {question}\nPolicy context:\n{context}\nTool result: {tool_result}"},
        ],
    )
    return response.choices[0].message.content or ""


# Run the RAG agent with external tools.
def main() -> None:
    client = create_client()
    question = input("Ask RAG/tool question: ").strip() or "Calculate 25 * 4 and tell me receipt rule."
    print("\nAgent:", ask_agent(client, question))


if __name__ == "__main__":
    main()

