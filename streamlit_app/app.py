
import os
import sys
import streamlit as st
from dotenv import load_dotenv

# 1️⃣ Load environment variables from .env (must be in project root)
load_dotenv()

# 2️⃣ Get your Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    st.error("GEMINI_API_KEY not found! Please check your .env file.")
    st.stop()

# 3️⃣ Add project root to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 4️⃣ Import project modules
from utils.config_loader import config
from core.query import RAGPipeline

# 5️⃣ Optional: override config key with environment variable if needed
config["gemini"]["api_key"] = GEMINI_API_KEY
# ---------------- Custom CSS ----------------
custom_css = """
<style>
    html {
        background-color: #1a202c;
        color: #e0e0e0;
        background-image:
            radial-gradient(ellipse at 50% 50%, rgba(255, 255, 255, 0.2) 1%, transparent 70%),
            radial-gradient(ellipse at 80% 20%, rgba(255, 255, 255, 0.1) 1%, transparent 80%),
            radial-gradient(ellipse at 20% 80%, rgba(255, 255, 255, 0.15) 1%, transparent 85%);
        background-size: 0.15rem 0.15rem, 0.1rem 0.1rem, 0.1rem 0.1rem;
        background-repeat: repeat;
        background-attachment: fixed;
    }
    
    [data-testid="stAppViewBlockContainer"] { background: transparent; }
    
    [data-testid="stAppViewBlockContainer"] h1 {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #e0e0e0;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    [data-testid="stChatMessage"][data-testid="stChatMessage-container-user"] {
        background-color: #e0f2ff;
        color: #333333;
    }
    
    [data-testid="stChatMessage"][data-testid="stChatMessage-container-assistant"] {
        background-color: #2d3748;
        color: #e0e0e0;
    }

    [data-testid="stChatInput"] input {
        background-color: #2d3748;
        color: #e0e0e0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
# ---------------- RAG Pipeline ----------------
@st.cache_resource
def get_rag_pipeline():
    try:
        # The initialization is now much simpler!
        return RAGPipeline()
    except Exception as e:
        st.error(f"Failed to initialize RAG pipeline: {e}")
        st.stop()


# ---------------- Main App ----------------
def main():
    st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'><span style='font-size:3rem;'>🤖</span> RAG Chatbot</h1>", unsafe_allow_html=True)
    st.write("Ask questions based on your knowledge base.")

    rag = get_rag_pipeline()

    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history
    for q, a in st.session_state.history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(a)

    # Get new user input
    query = st.chat_input("Enter your question here:")

    if query:
        # Add user's query to history
        st.session_state.history.append((query, ""))

        # Display spinner while generating answer
        with st.spinner("Generating answer..."):
            answer = rag.query(query, history=st.session_state.history[:-1])
            st.session_state.history[-1] = (query, answer)

        # No need to call st.rerun()


        # --- THIS IS THE FIX ---
        # Force the app to rerun from top to bottom to display the new message


if __name__ == "__main__":
    main()
