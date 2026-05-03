import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from app.rag.embeddings import get_embeddings
from sqlalchemy import text


def load_documents(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        loader = TextLoader(os.path.join(folder_path, file))
        docs.extend(loader.load())
    return docs


def create_vector_store(folder_path, embeddings):
    docs = load_documents(folder_path)
    return FAISS.from_documents(docs, embeddings)



def build_vendor_documents(db):
    records = db.execute(text("SELECT * FROM vendor_reputation")).fetchall()

    docs = []

    for r in records:
        data = r._mapping

        content = f"""
        Vendor ID: {data['vendor_id']}
        Issue: {data['issue']}
        Rating: {data['rating']}
        """

        docs.append(Document(page_content=content))

    return docs


def create_vendor_vector_store(db):
    embeddings = get_embeddings()
    docs = build_vendor_documents(db)

    return FAISS.from_documents(docs, embeddings)