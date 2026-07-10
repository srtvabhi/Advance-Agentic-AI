from models.state_models import ResilientState


async def validate_node(state: ResilientState) -> ResilientState:
    text = state["invoice_text"].lower()
    is_valid = "amount" in text and "vendor" in text

    if is_valid:
        return {"validation_status": "valid", "error": ""}

    return {
        "validation_status": "invalid",
        "error": "Invoice must include vendor and amount.",
    }

