import pytest
from faker import Faker

from django.utils.dateparse import parse_date

from accounts.api.v1.serializers import UserSerializer
from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


class TestUserSerializer:
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
        serializer = UserSerializer(instance=user, data=data)
        serializer.is_valid()
        updated_user = serializer.save()

        assert updated_user.email == user.email
        assert updated_user.first_name == user.first_name
        assert updated_user.last_name == user.last_name
        assert updated_user.avatar == user.avatar
        assert updated_user.birthdate == user.birthdate
        assert updated_user.gender == user.gender
        assert updated_user.about == user.about

    def test_data(self, user: User) -> None:
        serializer = UserSerializer(instance=user)

        assert serializer.data["first_name"] == user.first_name
        assert serializer.data["last_name"] == user.last_name
        assert serializer.data["avatar"] == user.avatar.url
        assert parse_date(serializer.data["birthdate"]) == user.birthdate
        assert serializer.data["gender"] == user.gender
        assert serializer.data["about"] == user.about
        for data, player_sport in zip(serializer.data["player"]["sports"], user.player.sports.all()):
            assert data["sport"]["value"] == player_sport.sport.name
            assert data["level"]["value"] == player_sport.level.level
