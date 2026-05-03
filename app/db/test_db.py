from app.db.database import SessionLocal
from app.db.models import Product, Inventory

db = SessionLocal()

product = db.query(Product).first()
inventory = db.query(Inventory).first()

print("Product:", product.name)
print("Stock:", inventory.current_stock)