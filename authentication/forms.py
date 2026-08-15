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
    class Meta:
        model = User
        fields = ('username',)
