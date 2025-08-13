from typing import List
import re


def clean_text(text: str) -> str:
    """
    Basic text cleaning: remove multiple newlines and extra spaces.
    """
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    Chunk text into overlapping chunks by word count.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        if end == len(words):
            break
        start += chunk_size - chunk_overlap
    return chunks
