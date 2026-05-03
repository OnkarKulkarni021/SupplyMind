from app.graph.graph_builder import build_graph
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.inventory_service import get_inventory_status
from app.services.procurement_service import select_best_vendor

router = APIRouter(tags=["Procurement"])


@router.post("/procure")
def trigger_procurement(db: Session = Depends(get_db)):
    inventory = get_inventory_status(db)

    if not inventory["is_low"]:
        return {"message": "Stock is sufficient. No procurement needed."}

    result = select_best_vendor(db)

    vendor = result["vendor"]

    return {
        "message": "Procurement triggered",
        "selected_vendor": {
            "id": vendor.id,
            "name": vendor.name,
            "score": result["score"]
        }
    }



@router.post("/run-agent")
def run_agent(db: Session = Depends(get_db)):
    graph = build_graph(db)

    result = graph.invoke({})

    return result