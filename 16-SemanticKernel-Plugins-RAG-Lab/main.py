import asyncio
import sys

from services.plugin_workflow import run_plugin_lab


DEFAULT_QUESTION = "Can I work from home three days a week, and when do I need manager approval?"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 16: Build AI Plugins Using Semantic Kernel\n")
    print("Enter a question, press Enter for the default question, or type 'quit' to exit.")

    while True:
        question = input(f"\nDefault question:\n{DEFAULT_QUESTION}\n\nQuestion: ").strip()

        if question.casefold() == "quit":
            print("Exiting Lab 16.")
            break

        question = question or DEFAULT_QUESTION
        print("\n" + await run_plugin_lab(question))


if __name__ == "__main__":
    asyncio.run(main())
