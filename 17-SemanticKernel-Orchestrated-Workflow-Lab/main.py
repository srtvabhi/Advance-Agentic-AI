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
    print("Enter a vendor request, press Enter for the default request, or type 'quit' to exit.")

    while True:
        request = input(f"\nDefault request:\n{DEFAULT_REQUEST}\n\nRequest: ").strip()

        if request.casefold() in {"quit", "exit"}:
            print("Exiting Lab 17.")
            break

        request = request or DEFAULT_REQUEST
        print("\n" + await run_vendor_workflow(request))


if __name__ == "__main__":
    asyncio.run(main())
