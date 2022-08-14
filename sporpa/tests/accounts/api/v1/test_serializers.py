import pytest
from faker import Faker

from accounts.api.v1.serializers import AuthTokenSerializer, UserCreateSerializer, UserUpdateSerializer
from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
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

    def test_validate_when_user_has_verified_email_is_false(self, unverified_user: User) -> None:
        data = {
            "email": unverified_user.email,
            "password": "testpassword",
        }
        serializer = AuthTokenSerializer(data=data)
        assert serializer.is_valid() is False


class TestUserCreateSerializer:
    def test_validate(self) -> None:
        user = UserFactory.build()
        data = {
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
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid() is True
        assert serializer.validated_data["email"] == user.email
        assert serializer.validated_data["password"] == user.password
        assert serializer.validated_data["first_name"] == user.first_name
        assert serializer.validated_data["last_name"] == user.last_name
        assert serializer.validated_data["avatar"] == user.avatar
        assert serializer.validated_data["birthdate"] == user.birthdate
        assert serializer.validated_data["gender"] == user.gender
        assert serializer.validated_data["about"] == user.about

    def test_validate_when_passwords_do_not_match(self) -> None:
        user = UserFactory.build()
        data = {
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
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid() is False

    def test_create(self) -> None:
        user = UserFactory.build()
        data = {
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
        serializer = UserCreateSerializer(data=data)
        serializer.is_valid()
        new_user = serializer.save()
        assert new_user.email == user.email
        assert new_user.first_name == user.first_name
        assert new_user.last_name == user.last_name
        assert new_user.avatar == user.avatar
        assert new_user.birthdate == user.birthdate
        assert new_user.gender == user.gender
        assert new_user.about == user.about


class TestUserUpdateSerializer:
    def test_update(self, user: User) -> None:
        user_factory = UserFactory.build()
        data = {
            "email": user_factory.email,
            "old_password": "testpassword",
            "password": user_factory.password,
            "password2": user_factory.password,
            "first_name": user_factory.first_name,
            "last_name": user_factory.last_name,
            "avatar": user_factory.avatar,
            "birthdate": user_factory.birthdate,
            "gender": user_factory.gender,
            "about": user_factory.about,
        }
        serializer = UserUpdateSerializer(instance=user, data=data)
        serializer.is_valid()
        updated_user = serializer.save()
        assert updated_user.email == user.email
        assert updated_user.first_name == user.first_name
        assert updated_user.last_name == user.last_name
        assert updated_user.avatar == user.avatar
        assert updated_user.birthdate == user.birthdate
        assert updated_user.gender == user.gender
        assert updated_user.about == user.about

    def test_validate_when_password_is_not_valid(self, user: User) -> None:
        user_factory = UserFactory.build()
        data = {
            "email": user_factory.email,
            "old_password": fake.password(),
            "password": user_factory.password,
            "password2": user_factory.password,
            "first_name": user_factory.first_name,
            "last_name": user_factory.last_name,
            "avatar": user_factory.avatar,
            "birthdate": user_factory.birthdate,
            "gender": user_factory.gender,
            "about": user_factory.about,
        }
        serializer = UserUpdateSerializer(instance=user, data=data)
        assert serializer.is_valid() is False

    def test_validate_when_passwords_do_not_match(self, user: User) -> None:
        user_factory = UserFactory.build()
        data = {
            "email": user_factory.email,
            "old_password": "testpassword",
            "password": user_factory.password,
            "password2": fake.password(),
            "first_name": user_factory.first_name,
            "last_name": user_factory.last_name,
            "avatar": user_factory.avatar,
            "birthdate": user_factory.birthdate,
            "gender": user_factory.gender,
            "about": user_factory.about,
        }
        serializer = UserUpdateSerializer(instance=user, data=data)
        assert serializer.is_valid() is False
