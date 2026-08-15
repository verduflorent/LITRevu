from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, SignupForm



def login_page(request):
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

    return render(
        request,
        'authentication/login.html',
        {'form': form},
    )

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
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
