# RAG Chatbot Project with BAAI Embeddings and Gemini

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system that:

- Extracts text from PDFs and DOCX documents (18 knowledge base files)
- Uses BAAI open-source embedding model for vector embeddings
- Stores embeddings in a FAISS vector database for similarity search
- Uses Gemini API for answer generation based on retrieved context
- Provides a Streamlit chatbot UI for real-time interaction

## Setup

1. Clone the repo and cd into `rag_project`

2. Put your 18 PDF and DOC files in `data/docs/`

3. Set your Gemini API key and other configs in `config/config.yaml`

4. Run setup script:

```bash
bash setup.sh
source venv/bin/activate
