# chroma_app/ models.py 
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    vector = models.BinaryField()  # Store the vector as binary data
    uploaded_at = models.DateTimeField(auto_now_add=True)


