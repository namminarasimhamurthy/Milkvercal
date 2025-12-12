"""
WSGI config for milk project.
Compatible with Vercel Python Runtime.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milk.settings')

# Django’s default WSGI application
application = get_wsgi_application()

# Vercel expects a callable named `app` or `handler`
app = application
handler = application
