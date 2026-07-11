import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load only this folder's .env file and create an OpenAI SDK client.
def create_client() -> OpenAI:
    load_dotenv(Path(__file__).with_name(".env"), override=True)
    return OpenAI(base_url=os.environ["AZURE_OPENAI_ENDPOINT"], api_key=os.environ["AZURE_OPENAI_API_KEY"])


# Function: call the model as a simple single agent.
def ask_agent(client: OpenAI, question: str) -> str:
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "You are a concise beginner-friendly assistant."},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message.content or ""


# Run the direct OpenAI SDK single-agent example.
def main() -> None:
    client = create_client()
    question = input("Ask a question: ").strip() or "Explain the OpenAI SDK in one paragraph."
    print("\nAgent:", ask_agent(client, question))


if __name__ == "__main__":
    main()

