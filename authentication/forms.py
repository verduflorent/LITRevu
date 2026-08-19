from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"

        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
