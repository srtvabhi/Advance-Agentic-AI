import asyncio
import sys

from config.settings import create_model_client
from orchestration.group_chat import create_group_chat
from services.output_service import format_team_messages


DEFAULT_TASK = (
    "Design a collaborative AutoGen solution for enterprise loan application processing. "
    "Include business workflow, technical architecture, security controls, and final recommendation."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 10: AutoGen Collaborative Multi-Agent Workflow\n")
    task = input(f"Enter task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    team = create_group_chat(model_client)

    try:
        result = await team.run(task=task)
        print("\n--- AutoGen Group Conversation ---\n")
        print(format_team_messages(result.messages))
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())

