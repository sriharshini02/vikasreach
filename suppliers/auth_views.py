from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout


# API-based Registration
@api_view(["POST"])
def register_user(request):
    """Register a new user via API"""
    data = request.data
    if User.objects.filter(username=data["username"]).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        username=data["username"],
        email=data["email"],
        password=make_password(data["password"]),
    )
    return Response(
        {"message": "User created successfully"}, status=status.HTTP_201_CREATED
    )


# Template-based Registration (for HTML forms)
def register(request):
    if request.method == "POST":
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
        messages.success(request, "Account created successfully!")
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
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to dashboard or home
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout
