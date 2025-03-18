# ollama_app/ urls.py 
from django.urls import path
from .views import chatbot_view, fetch_similarity_check, fetch_ollama_response, check_connection

urlpatterns = [
    path('', chatbot_view, name='chatbot_view'),
    path('fetch-similarity-check/', fetch_similarity_check, name='fetch_similarity_check'),
    path('fetch-ollama-response/', fetch_ollama_response, name='fetch_ollama_response'),
    path('check-connection/', check_connection, name='check_connection'),
]


