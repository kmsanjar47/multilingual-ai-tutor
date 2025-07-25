import re

def clean_text(text: str) -> str:
    # Replace multiple newlines, tabs, and spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove hyphenation at the end of lines
    text = re.sub(r'(\w)-(\s*\n\s*)', r'\1', text)
    return text
