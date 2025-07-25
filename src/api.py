from fastapi import FastAPI
from pydantic import BaseModel
from src.embed import get_embeddings
from src.vectorstore import load_vectorstore
from src.llm import get_llm
from src.chain import build_rag_chain
from src.config import TOP_K

app = FastAPI(title="Multilingual RAG (Bangla/English) - FAISS + Gemini")

emb = get_embeddings()
vs = load_vectorstore(emb)
retriever = vs.as_retriever(search_kwargs={"k": TOP_K})
llm = get_llm()
rag = build_rag_chain(llm, retriever)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    out = rag(q.question)
    return {
        "answer": out["answer"],
    }
