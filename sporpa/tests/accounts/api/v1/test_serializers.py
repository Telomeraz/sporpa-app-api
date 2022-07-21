import pytest

from accounts.api.v1.serializers import AuthTokenSerializer
from accounts.models import User

pytestmark = pytest.mark.django_db


class TestAuthTokenSerializer:
    def test_validate(self, user: User) -> None:
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["email"] == user.email
        assert serializer.validated_data["password"] == "testpassword"
        assert serializer.validated_data["user"] == user

    def test_validate_when_no_password(self) -> None:
        data = {
            "email": "qweasd@example.com",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False

    def test_validate_user_does_not_exist(self) -> None:
        data = {
            "email": "qweasd@example.com",
            "password": "qweasd",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False

    def test_validate_when_user_is_passive(self, passive_user: User) -> None:
        data = {
            "email": passive_user.email,
            "password": "testpassword",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False
