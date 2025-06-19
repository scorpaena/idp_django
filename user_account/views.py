from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from user_account.forms import SignupForm
from django.contrib.auth import login
# from allauth.account.forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

# def signup_login_view(request):
#     signup_form = SignupForm()
#     login_form = LoginForm()
#
#     if request.method == "POST" and 'login' not in request.path:
#         signup_form = SignupForm(request.POST)
#         if signup_form.is_valid():
#             user = signup_form.save(commit=False)
#             user.set_password(signup_form.cleaned_data["password"])
#             user.save()
#             login(request, user)
#             messages.success(request, "Signup successful!")
#             return redirect("home")
#         else:
#             messages.error(request, "Please correct the errors below.")
#
#     return render(request, "signup_login.html", {
#         "signup_form": signup_form,
#         "login_form": login_form
#     })

def signup_login_view(request):
    signup_form = SignupForm()
    login_form = AuthenticationForm()

    if request.method == "POST":
        if 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.set_password(signup_form.cleaned_data['password'])
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Please correct the errors below.")
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user(), backend='django.contrib.auth.backends.ModelBackend')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'signup_login.html', {
        'signup_form': signup_form,
        'login_form': login_form,
    })
