from app.rag.embeddings import get_embeddings
from app.rag.vector_store import create_vector_store
from app.rag.store import vendor_store
from app.rag.store import get_vendor_store

# Initialize once (simple MVP approach)
embeddings = get_embeddings()

vendor_store = create_vector_store(
    "app/rag/data/vendor_reputation",
    embeddings
)

policy_store = create_vector_store(
    "app/rag/data/procurement_policies",
    embeddings
)


def get_vendor_context(query):
    docs = vendor_store.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in docs])


def get_policy_context(query):
    docs = policy_store.similarity_search(query, k=2)
    return "\n".join([d.page_content for d in docs])


def build_vendor_documents(db):
    records = db.execute("SELECT * FROM vendor_reputation").fetchall()

    docs = []
    for r in records:
        text = f"""
        Vendor ID: {r.vendor_id}
        Rating: {r.rating}
        On-time Delivery: {r.on_time_delivery_rate}
        Defect Rate: {r.defect_rate}
        Notes: {r.notes}
        """
        docs.append(text)

    return docs



def get_vendor_context(query):
    store = get_vendor_store()

    docs = store.similarity_search(query, k=2)

    return "\n".join([d.page_content for d in docs])