from typing import Literal, TypedDict


class ResilientState(TypedDict, total=False):
    invoice_text: str
    extracted_data: str
    validation_status: Literal["valid", "invalid"]
    vendor_status: Literal["success", "failed"]
    retry_count: int
    error: str
    approval: str
    final_response: str

