import os
from chromadb import PersistentClient
from chromadb.config import Settings
from .chromadb_client import get_chromadb_client
from .utils import extract_text_from_pdf, split_text_into_chunks

# Create a ChromaDB client with the correct settings
client = PersistentClient(
    path=os.path.join(os.path.dirname(__file__), 'data', 'chroma_db'),
    settings=Settings(),
)
_, model = get_chromadb_client()

def add_document_to_chroma(pdf_path, document_name):
    try:
        # Try to get or create the collection
        collection = client.get_or_create_collection(name="consent_collection")

        # Check if document is already in the collection
        existing_ids = collection.get(ids=[f"{document_name}_0"])['ids']
        if existing_ids:
            print(f"Document '{document_name}' is already in ChromaDB, skipping.")
            return

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        chunks = split_text_into_chunks(extracted_text)

        # Generate embeddings for each chunk
        embeddings = model.encode(chunks).tolist()  # Convert embeddings to list

        # Prepare documents for upsert
        documents = []
        ids = []
        metadatas = []
        for i, chunk in enumerate(chunks):
            doc_id = f"{document_name}_{i}"
            documents.append(chunk)
            ids.append(doc_id)
            metadatas.append({"document_name": document_name, "chunk_id": i, "chunk_text": chunk})

        # Upsert documents into the collection
        collection.upsert(documents=documents, ids=ids, metadatas=metadatas, embeddings=embeddings)

        print(f"Document '{document_name}' added to ChromaDB.")

    except Exception as e:
        print(f"Error adding document to ChromaDB: {e}")

def load_chroma_from_initial_documents(initial_documents_dir):
    """Load data from initial documents into ChromaDB."""
    try:
        for filename in os.listdir(initial_documents_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(initial_documents_dir, filename)
                add_document_to_chroma(pdf_path, filename)
        print("Data loaded from initial documents into ChromaDB.")
    except Exception as e:
        print(f"Error loading data from initial documents: {e}")

def fetch_similar_documents(query_text, top_k=3):
    """Fetch similar documents from ChromaDB based on a query."""
    try:
        collection = client.get_collection(name="consent_collection")

        # Query the collection
        results = collection.query(query_texts=[query_text], n_results=top_k)

        # Extract similar documents from the results
        similar_texts = []
        for metadata_list in results['metadatas']:
            for metadata in metadata_list:
                similar_texts.append(metadata['chunk_text'])

        return similar_texts if similar_texts else ["No similar documents found."]
    except Exception as e:
        print(f"Error fetching similar documents: {e}")
        return ["Error occurred while fetching documents."]
