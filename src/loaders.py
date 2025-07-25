from langchain_community.document_loaders import PyMuPDFLoader
from src.utils import clean_text

def load_pdfs(paths: list[str]):
    docs = []
    for p in paths:
        loader = PyMuPDFLoader(p)
        for doc in loader.load():
            doc.page_content = clean_text(doc.page_content)
            docs.append(doc)
    return docs
