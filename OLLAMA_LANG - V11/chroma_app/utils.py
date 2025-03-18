# chroma_app/ utils.pu 

import pymupdf  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    document = pymupdf.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def split_text_into_chunks(text, chunk_size=500):
    """Split text into smaller chunks."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
