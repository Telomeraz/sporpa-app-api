import pytest

from accounts.api.v1.serializers import AuthTokenSerializer
from accounts.models import User

pytestmark = pytest.mark.django_db


class TestAuthTokenSerializer:
    def test_auth_token_serializer(self, user: User) -> None:
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["email"] == user.email
        assert serializer.validated_data["password"] == "testpassword"
        assert serializer.validated_data["user"] == user

    def test_auth_token_serializer_when_no_password(self) -> None:
        data = {
            "email": "qweasd@example.com",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False

    def test_auth_token_serializer_user_doesnt_exist(self) -> None:
        data = {
            "email": "qweasd@example.com",
            "password": "qweasd",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False

    def test_auth_token_serializer_when_user_is_passive(self, passive_user: User) -> None:
        data = {
            "email": passive_user.email,
            "password": "testpassword",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False
