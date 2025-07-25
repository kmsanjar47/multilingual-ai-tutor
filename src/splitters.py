from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def make_splitter():
    """
    This function creates a text splitter with separators optimized for both
    English and Bengali text. It uses a regex-based approach to handle
    various punctuation and whitespace, including the Zero-Width Joiner
    (u200d) which is critical for correct Bengali word formation.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Prioritize splitting on larger chunks of text first.
        # The regex handles Bengali (।), English punctuation, and whitespace.
        # The Zero-Width Joiner (\u200d) is included to prevent splitting in the middle of conjunct characters in Bengali.
        separators=["\n\n", "\n", "।", ".", "?", "!", " ", "-", "\t", "\u200d"],
        is_separator_regex=True,
    )

def split_docs(docs):
    """
    Splits a list of documents into smaller chunks while preserving metadata.
    """
    splitter = make_splitter()
    return splitter.split_documents(docs)


