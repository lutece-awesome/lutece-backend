"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import django
import os
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lutece.settings")
django.setup()
application = get_default_application()
