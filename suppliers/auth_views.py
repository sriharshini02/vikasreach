from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings
import requests


# Template-based Registration (for HTML forms)
def register_view(request):
    if request.method == "POST":
        # reCAPTCHA verification
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            "response": recaptcha_response,
        }
        recaptcha_verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data
        ).json()

        if not recaptcha_verify.get("success"):
            messages.error(request, "reCAPTCHA failed. Please confirm you are human.")
            return redirect("register")
        print("POST data received")  # Debug print
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        user.save()
        return redirect("login")

    return render(request, "register.html")


# Template-based Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to dashboard or home
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout
