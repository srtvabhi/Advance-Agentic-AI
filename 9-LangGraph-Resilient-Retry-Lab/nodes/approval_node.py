from models.state_models import ResilientState
from services.llm_service import ask_llm


async def approval_node(state: ResilientState) -> ResilientState:
    approval = await ask_llm(
        "You are a finance approval assistant.",
        (
            "Review this invoice and recommend approve, reject, or manual review.\n\n"
            f"Extracted data:\n{state['extracted_data']}\n\n"
            f"Vendor status:\n{state['error']}"
        ),
    )
    return {"approval": approval}

