"""Configuration de l'application d'authentification."""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Déclare l'application ``authentication`` auprès de Django."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
