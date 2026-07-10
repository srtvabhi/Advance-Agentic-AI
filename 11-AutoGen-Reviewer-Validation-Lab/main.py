import asyncio
import sys

from config.settings import create_model_client
from orchestration.review_workflow import run_review_workflow


DEFAULT_TASK = (
    "Create a one-page enterprise policy for AI agents that can access customer data "
    "and send external emails."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 11: AutoGen Reviewer Validation Pattern\n")
    task = input(f"Enter policy task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    try:
        result = await run_review_workflow(model_client, task)
        print("\n--- Validation Result ---\n")
        print(result.to_text())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
