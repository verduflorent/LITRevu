"""Point d'entrée ASGI du projet LITRevu.

La variable de module ``application`` est utilisée par les serveurs web
compatibles ASGI lors du déploiement.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
