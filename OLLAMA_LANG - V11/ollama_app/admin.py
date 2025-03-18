# ollama_app/admin.py
from django.contrib import admin
from .models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('text', 'response', 'created_at')
    search_fields = ('text',)
