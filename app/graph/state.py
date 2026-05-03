from typing import TypedDict, Optional

class ProcurementState(TypedDict):
    stock: int
    threshold: int
    is_low: bool

    selected_vendor: Optional[dict]
    approval_status: Optional[str]

    po_path: Optional[str]
    logistics_status: Optional[str]
    explanation: Optional[str]