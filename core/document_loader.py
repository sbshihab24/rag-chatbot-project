import os
import fitz  # PyMuPDF
from docx import Document
from typing import List, Tuple


def load_pdf_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def load_docx_text(docx_path: str) -> str:
    """
    Extract all text from a DOCX file.
    """
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def load_documents_from_folder(folder_path: str) -> List[Tuple[str, str]]:
    """
    Load all supported docs from folder. Return list of tuples (filename, text)
    Supports PDFs and DOCX files.
    """
    docs = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.lower().endswith(".pdf"):
            text = load_pdf_text(filepath)
            docs.append((filename, text))
        elif filename.lower().endswith(".docx") or filename.lower().endswith(".doc"):
            # For .doc files, user should convert to .docx or extend support with other libs.
            text = load_docx_text(filepath)
            docs.append((filename, text))
        else:
            # Unsupported file types are ignored
            continue
    return docs
