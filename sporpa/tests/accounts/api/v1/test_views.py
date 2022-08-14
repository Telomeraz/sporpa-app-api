import tempfile

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.api.v1.views import (
    AuthTokenView,
    RegisterView,
    SendEmailVerificationView,
    UpdateUserView,
    VerifyEmailView,
)
from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestAuthTokenView:
    def test_post(self, user: User) -> None:
        body = {
            "email": user.email,
            "password": "testpassword",
        }
        request = request_factory.post(reverse("api.v1.accounts:auth-token"), data=body)
        response = AuthTokenView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["token"] == user.auth_token.key

    def test_post_when_no_password(self) -> None:
        body = {
            "email": "qweasd@example.com",
        }
        request = request_factory.post(reverse("api.v1.accounts:auth-token"), data=body)
        response = AuthTokenView.as_view()(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_when_user_does_not_exist(self) -> None:
        body = {
            "email": "qweasd@example.com",
            "password": "qweasd",
        }
        request = request_factory.post(reverse("api.v1.accounts:auth-token"), data=body)
        response = AuthTokenView.as_view()(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_when_user_is_passive(self, passive_user: User) -> None:
        body = {
            "email": passive_user.email,
            "password": "testpassword",
        }
        request = request_factory.post(reverse("api.v1.accounts:auth-token"), data=body)
        response = AuthTokenView.as_view()(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestRegisterView:
    def test_post(self) -> None:
        user = UserFactory.build()
        body = {
            "email": user.email,
            "password": user.password,
            "password2": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": user.avatar,
            "birthdate": user.birthdate,
            "gender": user.gender,
            "about": user.about,
        }
        request = request_factory.post(reverse("api.v1.accounts:register"), data=body)
        response = RegisterView.as_view()(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=user.email).exists()

    def test_post_when_passwords_do_not_match(self) -> None:
        user = UserFactory.build()
        body = {
            "email": user.email,
            "password": user.password,
            "password2": fake.password(),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "avatar": user.avatar,
            "birthdate": user.birthdate,
            "gender": user.gender,
            "about": user.about,
        }
        request = request_factory.post(reverse("api.v1.accounts:register"), data=body)
        response = RegisterView.as_view()(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.filter(email=user.email).exists() is False


class TestUpdateUser:
    def test_put(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
        password = fake.password()
        with open(image_file.name, "rb") as data:
            body = {
                "email": fake.email(),
                "password": password,
                "password2": password,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "avatar": data,
                "birthdate": fake.date_of_birth(),
                "about": fake.text(max_nb_chars=User.about.field.max_length),
            }
            request = request_factory.put(
                reverse("api.v1.accounts:update-user"),
                data=body,
            )
        force_authenticate(request, user=user)
        response = UpdateUserView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
        with open(image_file.name, "rb") as data:
            body = {
                "avatar": data,
                "birthdate": fake.date_of_birth(),
                "about": fake.text(max_nb_chars=User.about.field.max_length),
            }
            request = request_factory.patch(
                reverse("api.v1.accounts:update-user"),
                data=body,
            )
        force_authenticate(request, user=user)
        response = UpdateUserView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK


class TestSendEmailVerificationView:
    def test_post(self, unverified_user: User) -> None:
        request = request_factory.post(
            reverse(
                "api.v1.accounts:send-email-verification",
                kwargs={"email": unverified_user.email},
            ),
        )
        response = SendEmailVerificationView.as_view()(request, unverified_user.email)
        assert response.status_code == status.HTTP_200_OK

    def test_post_when_user_does_not_exist(self) -> None:
        email = fake.email()
        request = request_factory.post(
            reverse(
                "api.v1.accounts:send-email-verification",
                kwargs={"email": email},
            ),
        )
        response = SendEmailVerificationView.as_view()(request, email)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_when_user_has_verified_email(self, user: User) -> None:
        request = request_factory.post(
            reverse(
                "api.v1.accounts:send-email-verification",
                kwargs={"email": user.email},
            ),
        )
        response = SendEmailVerificationView.as_view()(request, user.email)
        assert response.status_code == status.HTTP_409_CONFLICT


class TestVerifyEmailView:
    def test_post(self, unverified_user: User) -> None:
        token = unverified_user.make_token()
        request = request_factory.post(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": unverified_user.email},
            )
            + f"?token={token}",
        )
        response = VerifyEmailView.as_view()(request, unverified_user.email)
        unverified_user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert unverified_user.has_verified_email is True

    def test_post_when_user_has_verified_email(self, user: User) -> None:
        token = user.make_token()
        request = request_factory.post(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": user.email},
            )
            + f"?token={token}",
        )
        response = VerifyEmailView.as_view()(request, user.email)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_post_when_user_does_not_exist(self) -> None:
        email = fake.email()
        request = request_factory.post(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": email},
            ),
        )
        response = VerifyEmailView.as_view()(request, email)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_when_token_is_wrong(self, unverified_user: User) -> None:
        unverified_user.make_token()
        token = fake.password(40)
        request = request_factory.post(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": unverified_user.email},
            )
            + f"?token={token}",
        )
        response = VerifyEmailView.as_view()(request, unverified_user.email)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
