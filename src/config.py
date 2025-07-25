import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

VECTOR_DB = os.getenv("VECTOR_DB", "faiss")
FAISS_DIR = os.getenv("FAISS_DIR", ".faiss_store")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

TOP_K = int(os.getenv("TOP_K", 10))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))
