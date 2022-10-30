import pytest
from faker import Faker

from accounts.api.v1.serializers import UserUpdateSerializer
from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


class TestUserUpdateSerializer:
    def test_update(self, user: User) -> None:
        user_factory = UserFactory.build()
        data = {
            "email": user_factory.email,
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
