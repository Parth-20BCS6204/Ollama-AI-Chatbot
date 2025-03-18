# ollama_app/ models.py 
from django.db import models

class Query(models.Model):
    text = models.CharField(max_length=255)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
