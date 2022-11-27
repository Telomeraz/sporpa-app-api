import pytest

from accounts.models import User
from participants.api.v1.serializers import (
    PlayerSerializer,
    PlayerSportSerializer,
    SportLevelSerializer,
    SportSerializer,
)
from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db


class TestSportSerializer:
    def test_data(self) -> None:
        sport = Sport.objects.first()
        assert sport is not None
        data = {
            "value": sport.name,
            "display": sport.get_name_display(),
        }

        serializer = SportSerializer(sport)

        assert serializer.data == data


class TestSportLevelSerializer:
    def test_data(self) -> None:
        sport_level = SportLevel.objects.first()
        assert sport_level is not None
        data = {
            "value": sport_level.level,
            "display": sport_level.get_level_display(),
        }

        serializer = SportLevelSerializer(sport_level)

        assert serializer.data == data


class TestPlayerSportSerializer:
    def test_data(self, user: User) -> None:
        player_sport = user.player.sports.first()
        assert player_sport is not None
        data = {
            "sport": player_sport.sport_id,
            "level": player_sport.level_id,
        }

        serializer = PlayerSportSerializer(player_sport)

        assert serializer.data == data


class TestPlayerSerializer:
    def test_data(self, user: User) -> None:
        serializer = PlayerSerializer(user.player)

        for data, player_sport in zip(serializer.data["sports"], user.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id
