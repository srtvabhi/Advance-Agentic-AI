import asyncio
import sys

from services.plugin_workflow import run_plugin_lab


DEFAULT_QUESTION = "Can I work from home three days a week, and when do I need manager approval?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 16: Build AI Plugins Using Semantic Kernel\n")
    question = input(f"Enter question, or press Enter for default:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()
    question = question or DEFAULT_QUESTION

    print("\n" + await run_plugin_lab(question))


if __name__ == "__main__":
    asyncio.run(main())
