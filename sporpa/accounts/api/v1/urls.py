from allauth.account.views import confirm_email, email_verification_sent
from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView

from django.urls import path

from .views import UserUpdateView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="rest_login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="rest_logout",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="rest_register",
    ),
    path(
        "resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path(
        "confirm-email/<str:key>/",
        confirm_email,
        name="account_confirm_email",
    ),
    path(
        "confirm-email/",
        email_verification_sent,
        name="account_email_verification_sent",
    ),
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="rest_password_reset",
    ),
    path(
        "password/reset/<int:user_pk>/confirm/<str:key>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "user/update/",
        UserUpdateView.as_view(),
        name="user_update",
    ),
]
