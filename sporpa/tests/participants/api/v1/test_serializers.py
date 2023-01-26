import random

import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.models import User
from events.models import Activity
from participants.api.v1.serializers import (
    ParticipationRequestCreateSerializer,
    PlayerSerializer,
    PlayerSportSerializer,
    PlayerSportUpdateSerializer,
    SportLevelSerializer,
    SportSerializer,
)
from participants.models import ParticipationRequest, Sport, SportLevel

fake = Faker()
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


class TestPlayerSportUpdateSerializer:
    def test_update(self, user: User) -> None:
        player_sport = user.player.sports.first()
        sport = player_sport.sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user.player.pk,
            "level": sport_level.pk,
        }

        request = request_factory.put(
            reverse("participants:player_sports_update_level", kwargs={"sport_pk": sport.pk}),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = PlayerSportUpdateSerializer(instance=player_sport, data=data, context=context)
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


class TestParticipationRequestCreateSerializer:
    @pytest.mark.parametrize(
        "user, user2",
        [
            (
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 3},
                {"player__sports__level_id": 4, "player_sports_size": 1, "player__sports__sport_id": 3},
            ),
        ],
        indirect=["user", "user2"],
    )
    def test_create(self, user2: User, activity_without_players: Activity) -> None:
        message = fake.text(max_nb_chars=ParticipationRequest.message.field.max_length)
        data = {
            "activity": activity_without_players.pk,
            "message": message,
        }

        request = request_factory.post(
            reverse("participants:participation_requests"),
            data=data,
        )
        request.user = user2
        context = {
            "request": request,
        }
        serializer = ParticipationRequestCreateSerializer(data=data, context=context)
        assert serializer.is_valid()

        participation_request: ParticipationRequest = serializer.save()

        assert participation_request.activity == activity_without_players
        assert participation_request.participant == user2.player
        assert participation_request.message == message

    @pytest.mark.parametrize(
        "user, user2",
        [
            (
                {"player__sports__level_id": 2, "player_sports_size": 1, "player__sports__sport_id": 5},
                {"player__sports__level_id": 2, "player_sports_size": 1, "player__sports__sport_id": 5},
            ),
        ],
        indirect=["user", "user2"],
    )
    def test_create_when_participant_already_sent_participation_request(
        self,
        user2: User,
        activity_without_players: Activity,
    ) -> None:
        message = fake.text(max_nb_chars=ParticipationRequest.message.field.max_length)
        data = {
            "activity": activity_without_players.pk,
            "message": message,
        }

        request = request_factory.post(
            reverse("participants:participation_requests"),
            data=data,
        )
        request.user = user2
        context = {
            "request": request,
        }
        serializer = ParticipationRequestCreateSerializer(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        serializer = ParticipationRequestCreateSerializer(data=data, context=context)
        assert serializer.is_valid() is False
