from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("suppliers.urls")),  # Your app's routes
    path("accounts/", include("allauth.urls")),  # Handles login, logout, signup
    path("social/", include("social_django.urls", namespace="social")),  # Social logins
]
