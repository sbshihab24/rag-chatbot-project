# RAG Chatbot Project with BAAI Embeddings and Gemini

# RAG Chatbot Project

This is a **Retrieval-Augmented Generation (RAG) Chatbot** built with Python and Streamlit. The system allows users to ask questions based on a knowledge base of documents, leveraging vector embeddings, a Gemini API-powered LLM, and a local FAISS vector store.

---

## Features

- Load multiple document types (`PDF`, `DOCX`, `TXT`) into a knowledge base.
- Chunk documents and generate embeddings using **BAAI embedding model**.
- Store embeddings locally in a **FAISS vector store** for efficient retrieval.
- Query the knowledge base with natural language questions.
- Generate responses using **Gemini API**.
- Web interface built with **Streamlit**, supporting chat history.

---

## Project Structure
```
rag-chatbot-project/
│
├─ config/
│ ├─ config.yaml # Main configuration file
│ └─ gen-lang-client-*.json # Google service account (not pushed to GitHub)
│
├─ core/
│ ├─ query.py # Main RAG pipeline
│ ├─ embedder.py # Embedding logic
│ ├─ vector_store.py # FAISS vector storage
│ ├─ gemini_client.py # Gemini API wrapper
│ └─ text_chunker.py
│
├─ utils/
│ ├─ config_loader.py
│ ├─ file_utils.py
│ └─ logging_utils.py
│
├─ data/
│ └─ docs/ # Knowledge base documents
│
├─ embeddings_db/ # Local FAISS index and metadata
│
├─ streamlit_app/
│ └─ app.py # Streamlit chatbot frontend
│
├─ requirements.txt
├─ .env # Environment variables (not pushed)
└─ README.md
```



---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/your-username/rag-chatbot-project.git
cd rag-chatbot-project


## Dependencies

Python 3.11+

Streamlit

Transformers

PyYAML

FAISS

BAAI embedding model

## Author

Mehedi Hasan Shihab

LinkedIn: https://www.linkedin.com/in/shihab24

GitHub: https://github.com/sbshihab24
