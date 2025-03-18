# chatbot_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chroma_app.urls')),
    path('chroma/', include('chroma_app.urls')),
    path('ollama/', include('ollama_app.urls')),
]
