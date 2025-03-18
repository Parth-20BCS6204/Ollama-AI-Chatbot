# ollama_app/ tests.py 
from django.test import TestCase
import requests

class ChatbotTests(TestCase):
    def test_fetch_similar_documents(self):
        """Test fetching similar documents from chroma_app."""
        response = requests.post('http://localhost:8001/fetch-similar-documents/', json={'query_text': 'sample query'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('documents', response.json())

    def test_get_response(self):
        """Test getting a response from Ollama model."""
        response = requests.post('http://localhost:8002/', data={'prompt': 'sample prompt'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bot_response', response.json())
