from pydantic import BaseModel

class InventoryResponse(BaseModel):
    product_id: int
    product_name: str
    current_stock: int
    threshold: int


class VendorResponse(BaseModel):
    id: int
    name: str
    score: float


class ProcurementResponse(BaseModel):
    selected_vendor: VendorResponse
    message: str