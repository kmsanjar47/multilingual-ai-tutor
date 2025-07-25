import yaml
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from src.embed import get_embeddings
from src.vectorstore import load_vectorstore
from src.llm import get_llm
from src.chain import build_rag_chain
from src.config import TOP_K

def cosine_sim(a, b):
    return float(cosine_similarity(a, b)[0][0])

def main():
    with open("tests/sample_questions.yaml") as f:
        cases = yaml.safe_load(f)

    emb = get_embeddings()
    vs = load_vectorstore(emb)
    retriever = vs.as_retriever(search_kwargs={"k": TOP_K})
    llm = get_llm()
    rag = build_rag_chain(llm, retriever)

    sent_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    for c in cases:
        q = c["q"]
        gold = c["gold"]
        out = rag(q)
        ans = out["result"]
        s = cosine_sim(
            sent_model.encode([ans]),
            sent_model.encode([gold])
        )
        print({"q": q, "ans": ans, "gold": gold, "semantic_sim": round(s, 4)})

if __name__ == "__main__":
    main()
