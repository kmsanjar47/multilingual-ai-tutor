from langchain_community.vectorstores import FAISS
from src.config import VECTOR_DB, FAISS_DIR

def build_or_load_vectorstore(docs, embeddings):
    if VECTOR_DB != "faiss":
        raise ValueError("This template is configured only for FAISS right now.")
    vs = FAISS.from_documents(docs, embeddings)
    vs.save_local(FAISS_DIR)
    return vs

def load_vectorstore(embeddings):
    if VECTOR_DB != "faiss":
        raise ValueError("This template is configured only for FAISS right now.")
    # allow_dangerous_deserialization is needed for FAISS load_local in LangChain
    return FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
