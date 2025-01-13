import os

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://13.126.129.9:11434')
EMBEDDING_MODEL = 'CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'bartowski/Llama-3.2-1B-Instruct-GGUF'