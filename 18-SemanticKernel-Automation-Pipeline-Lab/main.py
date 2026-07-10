import asyncio
import sys

from services.automation_pipeline import run_change_pipeline


DEFAULT_CHANGE = (
    "Deploy a production firewall rule change for the payment API during the weekend "
    "maintenance window."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 18: Semantic Kernel Multi-Step AI Automation Pipeline\n")
    change = input(f"Enter change request, or press Enter for default:\n{DEFAULT_CHANGE}\n\nChange: ").strip()
    change = change or DEFAULT_CHANGE
    print("\n" + await run_change_pipeline(change))


if __name__ == "__main__":
    asyncio.run(main())
