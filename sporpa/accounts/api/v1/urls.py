from allauth.account.views import confirm_email, email_verification_sent
from allauth.socialaccount.views import connections, login_cancelled, login_error, signup
from dj_rest_auth.registration.views import RegisterView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView

from django.urls import path

from .views import GoogleLoginView, UserRetrieveUpdateView

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
        "login/google/",
        GoogleLoginView.as_view(),
        name="google_login",
    ),
    path(
        "login/cancelled/",
        login_cancelled,
        name="socialaccount_login_cancelled",
    ),
    path(
        "login/error/",
        login_error,
        name="socialaccount_login_error",
    ),
    path(
        "signup/",
        signup,
        name="socialaccount_signup",
    ),
    path(
        "connections/",
        connections,
        name="socialaccount_connections",
    ),
    path(
        "users/",
        UserRetrieveUpdateView.as_view(http_method_names=("post", "put")),
        name="accounts-users",
    ),
    path(
        "users/<int:pk>/",
        UserRetrieveUpdateView.as_view(http_method_names=("get",)),
        name="accounts-users",
    ),
]
