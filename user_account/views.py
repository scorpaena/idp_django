from django.shortcuts import render, redirect
from django.contrib import messages
from user_account.forms import SignupForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

def signup_view(request):
    signup_form = SignupForm()

    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.error(request, "Please correct the errors below.")

    return render(request, 'signup.html', {'signup_form': signup_form})


def login_view(request):
    login_form = AuthenticationForm()

    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user(), backend='django.contrib.auth.backends.ModelBackend')
            return redirect(settings.LOGIN_REDIRECT_URL)
        messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'login_form': login_form})
