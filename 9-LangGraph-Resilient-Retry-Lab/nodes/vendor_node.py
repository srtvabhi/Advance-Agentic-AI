from models.state_models import ResilientState
from services.vendor_service import TemporaryVendorError, verify_vendor


async def vendor_node(state: ResilientState) -> ResilientState:
    retry_count = state.get("retry_count", 0)

    try:
        status = verify_vendor(retry_count)
        return {
            "vendor_status": "success",
            "error": status,
            "retry_count": retry_count,
        }
    except TemporaryVendorError as exc:
        return {
            "vendor_status": "failed",
            "error": str(exc),
            "retry_count": retry_count + 1,
        }

