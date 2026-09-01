"""Configuration de l'application de gestion des critiques."""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Déclare l'application ``reviews`` auprès de Django."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
