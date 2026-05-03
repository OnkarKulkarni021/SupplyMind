from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    threshold = Column(Integer)


class Inventory(Base):
    __tablename__ = "inventory"

    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    current_stock = Column(Integer)


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    distance = Column(Float)
    lead_time = Column(Integer)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    status = Column(String)
    po_path = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class LogisticsUpdate(Base):
    __tablename__ = "logistics_updates"

    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"))
    status = Column(String)
    timestamp = Column(TIMESTAMP, server_default=func.now())