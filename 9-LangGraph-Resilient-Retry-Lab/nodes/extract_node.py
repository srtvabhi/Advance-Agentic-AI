from models.state_models import ResilientState
from services.llm_service import ask_llm


async def extract_node(state: ResilientState) -> ResilientState:
    extracted_data = await ask_llm(
        "You extract invoice fields.",
        f"Extract vendor, amount, due date, and risk notes from this invoice:\n{state['invoice_text']}",
    )
    return {"extracted_data": extracted_data}

