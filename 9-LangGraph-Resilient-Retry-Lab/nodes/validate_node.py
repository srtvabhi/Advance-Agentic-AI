from models.state_models import ResilientState


async def validate_node(state: ResilientState) -> ResilientState:
    text = state["invoice_text"].lower()
    has_vendor_field = "vendor:" in text
    has_amount_field = "amount:" in text
    is_valid = has_vendor_field and has_amount_field

    if is_valid:
        return {"validation_status": "valid", "error": ""}

    missing_fields = []
    if not has_vendor_field:
        missing_fields.append("Vendor")
    if not has_amount_field:
        missing_fields.append("Amount")

    return {
        "validation_status": "invalid",
        "error": f"Invoice is missing required field(s): {', '.join(missing_fields)}.",
    }
