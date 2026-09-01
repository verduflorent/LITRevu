"""Point d'entrée WSGI du projet LITRevu.

La variable de module ``application`` est utilisée par les serveurs web
compatibles WSGI lors du déploiement.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
