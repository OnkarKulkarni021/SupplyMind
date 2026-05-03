from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import SessionLocal
from app.rag.vector_store import create_vendor_vector_store
from app.rag.store import set_vendor_store
from app.api.v1 import inventory, procurement

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()

    vendor_store = create_vendor_vector_store(db)
    set_vendor_store(vendor_store)

    db.close()

    print("✅ RAG Initialized")

    yield

    # 🔻 Shutdown logic (optional)
    print("App shutting down")


app = FastAPI(lifespan=lifespan)

app.include_router(inventory.router, prefix="/api/v1")
app.include_router(procurement.router, prefix="/api/v1")