"""Modèle utilisateur de l'application."""

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Utilisateur LITRevu, fondé sur le modèle d'authentification Django."""

    pass
