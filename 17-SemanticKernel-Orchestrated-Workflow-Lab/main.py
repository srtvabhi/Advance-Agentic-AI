import asyncio
import sys

from services.orchestrated_workflow import run_vendor_workflow


DEFAULT_REQUEST = (
    "Contoso Insights wants production API access to customer data for analytics "
    "and will store exports in its cloud platform."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 17: Semantic Kernel Orchestrated AI Workflow\n")
    request = input(f"Enter vendor request, or press Enter for default:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()
    request = request or DEFAULT_REQUEST
    print("\n" + await run_vendor_workflow(request))


if __name__ == "__main__":
    asyncio.run(main())
