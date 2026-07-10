from models.state_models import ResilientState


async def final_node(state: ResilientState) -> ResilientState:
    if state.get("validation_status") == "invalid":
        return {"final_response": f"Workflow stopped: {state['error']}"}

    if state.get("vendor_status") == "failed":
        return {"final_response": f"Workflow failed after retries: {state['error']}"}

    return {
        "final_response": (
            "Resilient workflow completed.\n\n"
            f"Retries used: {state.get('retry_count', 0)}\n\n"
            f"Extracted data:\n{state['extracted_data']}\n\n"
            f"Approval recommendation:\n{state['approval']}"
        )
    }

