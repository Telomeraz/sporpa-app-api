import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.api.v1.views import AuthTokenView
from accounts.models import User

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
