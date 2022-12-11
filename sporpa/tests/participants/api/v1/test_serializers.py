import random

import pytest
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.models import User
from participants.api.v1.serializers import (
    PlayerSerializer,
    PlayerSportSerializer,
    PlayerSportUpdateLevelSerializer,
    SportLevelSerializer,
    SportSerializer,
)
from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


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
            "player": user.player.pk,
            "sport": player_sport.sport_id,
            "level": player_sport.level_id,
        }

        serializer = PlayerSportSerializer(player_sport)
        data.pop("player")

        assert serializer.data == data

    def test_create(self, user_without_sport: User) -> None:
        sport = random.choice(Sport.objects.all())
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user_without_sport.player.pk,
            "sport": sport.pk,
            "level": sport_level.pk,
        }

        request = request_factory.post(
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user_without_sport
        context = {
            "request": request,
        }
        serializer = PlayerSportSerializer(data=data, context=context)
        assert serializer.is_valid()

        player_sport = serializer.save()

        assert player_sport.sport == sport
        assert player_sport.level == sport_level

    def test_create_when_has_same_sport(self, user: User) -> None:
        sport = user.player.sports.first().sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user.player.pk,
            "sport": sport.pk,
            "level": sport_level.pk,
        }

        request = request_factory.post(
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = PlayerSportSerializer(data=data, context=context)

        assert serializer.is_valid() is False


class TestPlayerSportUpdateLevelSerializer:
    def test_update(self, user: User) -> None:
        player_sport = user.player.sports.first()
        sport = player_sport.sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user.player.pk,
            "level": sport_level.pk,
        }

        request = request_factory.put(
            reverse("participants:player_sports_update_level", kwargs={"sport_id": sport.pk}),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = PlayerSportUpdateLevelSerializer(instance=player_sport, data=data, context=context)
        assert serializer.is_valid()

        player_sport = serializer.save()

        assert player_sport.sport == sport
        assert player_sport.level == sport_level


class TestPlayerSerializer:
    def test_data(self, user: User) -> None:
        serializer = PlayerSerializer(user.player)

        for data, player_sport in zip(serializer.data["sports"], user.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id
