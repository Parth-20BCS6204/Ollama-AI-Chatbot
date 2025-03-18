# chroma_app/ tests.py 
import os
from django.conf import settings
from .vector_store import add_document_to_chroma
from .utils import extract_text_from_pdf

def initialize_chroma_with_documents():
    initial_documents_dir = os.path.join(settings.BASE_DIR, 'initial_documents')

    if not os.path.exists(initial_documents_dir):
        print(f"Initial documents directory '{initial_documents_dir}' not found.")
        return

    print("Initializing ChromaDB with documents...")

    for filename in os.listdir(initial_documents_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(initial_documents_dir, filename)
            add_document_to_chroma(pdf_path, filename)
