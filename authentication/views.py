"""Vues responsables de l'inscription et de la gestion des sessions."""

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm


def login_page(request):
    """Authentifie un utilisateur puis le redirige vers son flux."""
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect('feed')

            form.add_error(
                None,
                "Nom d'utilisateur ou mot de passe incorrect."
            )

    return render(
        request,
        'authentication/login.html',
        {'form': form},
    )


def logout_user(request):
    """Ferme la session courante et renvoie vers la page de connexion."""
    logout(request)
    return redirect('login')


def signup_page(request):
    """Crée un compte utilisateur à partir des données valides du formulaire."""
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    return render(
        request,
        'authentication/signup.html',
        {'form': form},
    )
