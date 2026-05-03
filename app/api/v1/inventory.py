from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.inventory_service import get_inventory_status

router = APIRouter(tags=["Inventory"])


@router.get("/inventory")
def check_inventory(db: Session = Depends(get_db)):
    return get_inventory_status(db)