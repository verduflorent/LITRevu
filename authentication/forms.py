"""Formulaires utilisés pour la connexion et la création d'un compte."""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(forms.Form):
    """Collecte les identifiants nécessaires à l'authentification."""
    username = forms.CharField(max_length=63)
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput,
    )


class SignupForm(UserCreationForm):
    """Adapte le formulaire Django de création d'utilisateur à LITRevu."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        """Traduit les libellés et masque les aides génériques de Django."""
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
