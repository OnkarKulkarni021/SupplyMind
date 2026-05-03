from sqlalchemy.orm import Session
from app.services.inventory_service import get_inventory_status
from app.services.procurement_service import select_best_vendor
from app.rag.retriever import get_vendor_context, get_policy_context
from app.llm.chains import generate_explanation

def check_inventory_node(state, db: Session):
    data = get_inventory_status(db)

    return {
        "stock": data["current_stock"],
        "threshold": data["threshold"],
        "is_low": data["is_low"]
    }


def procurement_node(state, db):
    result = select_best_vendor(db)
    vendor = result["vendor"]

    vendor_context = get_vendor_context(vendor.name)
    policy_context = get_policy_context("vendor selection policy")

    explanation = generate_explanation({
        "vendor_name": vendor.name,
        "score": result["score"],
        "vendor_context": vendor_context,
        "policy_context": policy_context
    })

    return {
        "selected_vendor": {
            "id": vendor.id,
            "name": vendor.name,
            "score": result["score"]
        },
        "explanation": explanation
    }


def approval_node(state):
    # Later this will come from UI
    return {
        "approval_status": "pending"
    }


def send_po_node(state):
    return {
        "po_path": "/tmp/sample_po.pdf"
    }


def logistics_node(state):
    return {
        "logistics_status": "PLACED"
    }