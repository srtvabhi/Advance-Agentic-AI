import asyncio
import sys

from graph.orchestration_graph import build_graph


DEFAULT_PROBLEM = (
    "Design an enterprise IT service desk workflow that classifies tickets, "
    "routes incidents, escalates urgent issues, and creates a final resolution summary."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 7: LangGraph Multi-Step Orchestration\n")
    problem = input(f"Enter problem, or press Enter for default:\n{DEFAULT_PROBLEM}\n\nProblem: ").strip()
    problem = problem or DEFAULT_PROBLEM

    app = build_graph()
    result = await app.ainvoke({"problem": problem})

    print("\n--- Requirements ---\n")
    print(result["requirements"])
    print("\n--- Plan ---\n")
    print(result["plan"])
    print("\n--- Execution ---\n")
    print(result["execution"])
    print("\n--- Final Summary ---\n")
    print(result["summary"])


if __name__ == "__main__":
    asyncio.run(main())

