from django.urls import path

from .views import AuthTokenView, RegisterView, SendEmailVerificationView, UpdateUserView, VerifyEmailView

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
        SendEmailVerificationView.as_view(),
        name="send-verification-email",
    ),
    path(
        "user/verify-email/<str:email>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
]
