from sqlalchemy.orm import Session
from app.db import models

def get_inventory_status(db: Session):
    product = db.query(models.Product).first()
    inventory = db.query(models.Inventory).first()

    return {
        "product_id": product.id,
        "product_name": product.name,
        "current_stock": inventory.current_stock,
        "threshold": product.threshold,
        "is_low": inventory.current_stock < product.threshold
    }