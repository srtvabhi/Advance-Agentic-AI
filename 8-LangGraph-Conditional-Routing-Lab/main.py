import asyncio
import sys

from graph.routing_graph import build_graph


DEFAULT_QUESTION = "What security controls are needed for a payroll automation agent?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 8: LangGraph Conditional Agent Routing\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    app = build_graph()
    result = await app.ainvoke({"question": question})

    print("\n--- Final Response ---\n")
    print(result["final_response"])


if __name__ == "__main__":
    asyncio.run(main())

