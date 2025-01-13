# config.py
import streamlit as st

# Fetch secrets stored in Streamlit
OLLAMA_HOST = st.secrets["ollama_host"]
EMBEDDING_MODEL = st.secrets["embedding_model"]
LANGUAGE_MODEL = st.secrets["language_model"]
