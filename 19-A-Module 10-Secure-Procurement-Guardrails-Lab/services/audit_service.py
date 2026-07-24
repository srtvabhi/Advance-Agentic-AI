import hashlib
from datetime import datetime, timezone
from typing import Any

from models.procurement_models import ProcurementState


# Return a UTC timestamp for every control event in the workflow.
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# Store only a stable hash of user identities in the audit log.
def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


# Append one audit event and return the full updated audit log.
def audit_event(state: ProcurementState, node: str, decision: str, **details: Any) -> list[dict[str, Any]]:
    log = list(state.get("audit_log", []))
    log.append(
        {
            "timestamp": utc_now(),
            "node": node,
            "decision": decision,
            "request_id": state["request_id"],
            "requester_id_hash": stable_hash(state["requester_id"]),
            **details,
        }
    )
    return log
