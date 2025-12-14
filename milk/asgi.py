import os
from django.core.asgi import get_asgi_application
from mangum import Mangum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "milk.settings")

django_asgi_app = get_asgi_application()

# ✅ THIS is what Vercel expects
handler = Mangum(django_asgi_app)
