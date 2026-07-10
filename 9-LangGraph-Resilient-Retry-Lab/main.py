import asyncio
import sys

from graph.resilient_graph import build_graph


DEFAULT_INVOICE = (
    "Vendor: Contoso Cloud Services. Amount: 15000 USD. "
    "Due date: 2026-08-15. Purpose: Annual cloud monitoring renewal."
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def main() -> None:
    print("Lab 9: LangGraph Resilient Workflow With Retries\n")
    invoice = input(f"Enter invoice text, or press Enter for default:\n{DEFAULT_INVOICE}\n\nInvoice: ").strip()
    invoice = invoice or DEFAULT_INVOICE

    app = build_graph()
    result = await app.ainvoke(
        {"invoice_text": invoice, "retry_count": 0},
        config={"configurable": {"thread_id": "invoice-demo-1"}},
    )

    print("\n--- Final Response ---\n")
    print(result["final_response"])


if __name__ == "__main__":
    asyncio.run(main())

