from django.urls import path

from .views import (
    AuthTokenView,
    RegisterView,
    ResetPasswordView,
    SendPasswordResetEmailView,
    SendVerificationEmailView,
    UpdateUserView,
    VerifyEmailView,
)

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
    path(
        "user/send-verification-email/<str:email>/",
        SendVerificationEmailView.as_view(),
        name="send-verification-email",
    ),
    path(
        "user/verify-email/<str:email>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "user/send-password-reset-email/<str:email>/",
        SendPasswordResetEmailView.as_view(),
        name="send-password-reset-email",
    ),
    path(
        "user/reset-password/<str:email>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
