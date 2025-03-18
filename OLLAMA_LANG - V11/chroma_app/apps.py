from django.apps import AppConfig
import os
from django.conf import settings
from .vector_store import load_chroma_from_initial_documents

class ChromaAppConfig(AppConfig):
    name = 'chroma_app'

    def ready(self):
        # Initialize Chroma with documents if the database is empty
        self.initialize_chroma_with_documents()

    def initialize_chroma_with_documents(self):
        initial_documents_dir = os.path.join(settings.BASE_DIR, 'initial_documents')

        if not os.path.exists(initial_documents_dir):
            print(f"Initial documents directory '{initial_documents_dir}' not found.")
            return

        print("Initializing ChromaDB with documents...")

        load_chroma_from_initial_documents(initial_documents_dir)

        print("Initialization complete.")
