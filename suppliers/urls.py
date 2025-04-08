from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home
from .auth_views import register_view, login_view
from .auth_views import logout_view
from django.urls import path
from .views import contact_view, about_view


urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path("about/", about_view, name="about"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register_view, name="register"),  # HTML form-based registeration
    path("login/", login_view, name="login"),  # HTML form-based login
]
