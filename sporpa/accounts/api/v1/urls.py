from django.urls import path

from .views import AuthTokenView, RegisterView, UpdateUserView

app_name = "api.v1.accounts"
urlpatterns = [
    path(
        "auth-token/",
        AuthTokenView.as_view(),
        name="auth-token",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "user/update/",
        UpdateUserView.as_view(),
        name="update-user",
    ),
]
