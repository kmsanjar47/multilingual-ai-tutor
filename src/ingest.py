import argparse
import glob
from src.loaders import load_pdfs
from src.splitters import split_docs
from src.embed import get_embeddings
from src.vectorstore import build_or_load_vectorstore

def main(pdf_globs):
    paths = []
    for g in pdf_globs:
        paths.extend(glob.glob(g))
    if not paths:
        raise ValueError("No PDFs found")

    print(f"Loading {len(paths)} pdf(s)...")
    docs = load_pdfs(paths)

    print("Splitting...")
    chunks = split_docs(docs)
    print(f"Chunks: {len(chunks)}")

    print("Embedding & saving FAISS...")
    emb = get_embeddings()
    build_or_load_vectorstore(chunks, emb)

    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", nargs="+", default=["data/*.pdf"])
    args = parser.parse_args()
    main(args.pdfs)
