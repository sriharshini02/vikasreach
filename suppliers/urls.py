from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home
from .auth_views import register_view, login_view
from .auth_views import logout_view
from django.urls import path
from .views import contact_view, about_view


urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact_view, name="contact"),
    path("about/", about_view, name="about"),
    # Custom auth views
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    # JWT endpoints
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
