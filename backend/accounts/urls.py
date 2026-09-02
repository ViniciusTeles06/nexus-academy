from django.urls import path

from .views import (
    GoogleLoginView,
    LoginView,
    LogoutView,
    MeView,
    RefreshView,
)


urlpatterns = [
    path(
        "auth/login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "auth/google/",
        GoogleLoginView.as_view(),
        name="google-login",
    ),

    path(
        "auth/refresh/",
        RefreshView.as_view(),
        name="refresh",
    ),

    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "auth/me/",
        MeView.as_view(),
        name="me",
    ),
]