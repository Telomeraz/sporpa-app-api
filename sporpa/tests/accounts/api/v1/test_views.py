import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.api.v1.views import AuthTokenView, RegisterView
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

    def test_post_user_doesnt_exist(self) -> None:
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
