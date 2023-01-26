import pytest
from faker import Faker

from django.utils.dateparse import parse_date

from accounts.api.v1.serializers import UserRetrieveUpdateSerializer
from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


class TestUserRetrieveUpdateSerializer:
    def test_update(self, user: User) -> None:
        another_user = UserFactory()
        data = {
            "email": another_user.email,
            "first_name": another_user.first_name,
            "last_name": another_user.last_name,
            "avatar": another_user.avatar,
            "birthdate": another_user.birthdate,
            "gender": another_user.gender,
            "about": another_user.about,
        }
        serializer = UserRetrieveUpdateSerializer(instance=user, data=data)
        assert serializer.is_valid()

        updated_user = serializer.save()

        assert updated_user.email == user.email
        assert updated_user.first_name == user.first_name
        assert updated_user.last_name == user.last_name
        assert updated_user.avatar == user.avatar
        assert updated_user.birthdate == user.birthdate
        assert updated_user.gender == user.gender
        assert updated_user.about == user.about

    def test_data(self, user: User) -> None:
        serializer = UserRetrieveUpdateSerializer(instance=user)

        assert serializer.data["first_name"] == user.first_name
        assert serializer.data["last_name"] == user.last_name
        assert serializer.data["avatar"] == user.avatar.url
        assert parse_date(serializer.data["birthdate"]) == user.birthdate
        assert serializer.data["gender"] == user.gender
        assert serializer.data["about"] == user.about
        for data, player_sport in zip(serializer.data["player"]["sports"], user.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id
