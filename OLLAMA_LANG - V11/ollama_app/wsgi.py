# ollama_app/ wsgi.py 

"""
WSGI config for ollama_app.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ollama_app.settings')

application = get_wsgi_application()
