# chroma_app / chromadb_client.py
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
client = chromadb.Client()

# Initialize Sentence Transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

import chromadb
chroma_client = chromadb.Client()

def get_chromadb_client():
    return client, model
