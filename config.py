# config.py
import streamlit as st

# Fetch secrets stored in Streamlit
OLLAMA_HOST = st.secrets["OLLAMA_HOST"]
EMBEDDING_MODEL = st.secrets["EMBEDDING_MODEL"]
LANGUAGE_MODEL = st.secrets["LANGUAGE_MODEL"]
