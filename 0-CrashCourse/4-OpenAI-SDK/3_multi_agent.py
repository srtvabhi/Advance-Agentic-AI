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


# Function: call the model as a role-specific agent.
def call_agent(client: OpenAI, role: str, instruction: str, content: str) -> str:
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content or ""


# Coordinate planner, executor, and reviewer using direct SDK calls.
def main() -> None:
    client = create_client()
    task = input("Enter enterprise task: ").strip() or "Create a sales lead qualification workflow."
    plan = call_agent(client, "planner", "You are a planner. Create 5 short steps.", task)
    execution = call_agent(client, "executor", "You are an executor. Add actions and owners.", plan)
    review = call_agent(client, "reviewer", "You are a reviewer. Identify risks and missing approvals.", execution)

    print("\n--- Planner ---\n", plan)
    print("\n--- Executor ---\n", execution)
    print("\n--- Reviewer ---\n", review)


if __name__ == "__main__":
    main()

