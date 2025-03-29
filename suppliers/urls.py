from django.urls import path
from .views import (
    ManufacturerListCreateView,
    ManufacturerDetailView,
    ProductListCreateView,
    ProductDetailView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import scrape_view, home
from .auth_views import register_user, register, login_view
from .auth_views import logout_view
from django.urls import path
from .views import contact_view, about_view


urlpatterns = [
    path("contact/", contact_view, name="contact"),
    path("about/", about_view, name="about"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("scrape/", scrape_view, name="scrape"),
    path(
        "manufacturers/", ManufacturerListCreateView.as_view(), name="manufacturer-list"
    ),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register, name="register"),  # HTML form-based register
    path("api/register/", register_user, name="api-register"),  # API register
    path("login/", login_view, name="login"),  # HTML form-based login
]
