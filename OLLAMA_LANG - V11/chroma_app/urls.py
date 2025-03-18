# chroma_app/ urls.py 
from django.urls import path
from .views import upload_document, fetch_similar_documents_view

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('fetch-similar-documents/', fetch_similar_documents_view, name='fetch_similar_documents'),
]
