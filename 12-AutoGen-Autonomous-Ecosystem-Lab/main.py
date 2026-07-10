import asyncio
import sys

from config.settings import create_model_client
from orchestration.ecosystem_chat import create_incident_ecosystem
from services.output_service import format_transcript


DEFAULT_TASK = (
    "The payment API is slow and customers are reporting checkout failures. "
    "Autonomously investigate, open an incident, notify the team, analyze cause, and prepare an update."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 12: AutoGen Autonomous Task-Solving Ecosystem\n")
    task = input(f"Enter incident task, or press Enter for default:\n{DEFAULT_TASK}\n\nTask: ").strip()
    task = task or DEFAULT_TASK

    model_client = create_model_client()
    team = create_incident_ecosystem(model_client)

    try:
        result = await team.run(task=task)
        print("\n--- Autonomous Ecosystem Transcript ---\n")
        print(format_transcript(result.messages).to_text())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())

