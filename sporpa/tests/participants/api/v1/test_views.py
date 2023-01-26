import random

import pytest
from faker import Faker
from rest_framework import status as http_status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from events.models import Activity
from participants.api.v1.views import (
    ParticipationRequestCreateView,
    PlayerSportCreateView,
    PlayerSportUpdateView,
    SportLevelListView,
    SportListView,
)
from participants.models import ParticipationRequest, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestSportListView:
    def test_list(self, user: User) -> None:
        request = request_factory.get(
            reverse("participants:sports"),
        )
        force_authenticate(request, user=user)
        response = SportListView.as_view()(request)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["results"]
        for data, sport in zip(response.data["results"], Sport.objects.all()):
            assert data["value"] == sport.pk
            assert data["display"] == sport.get_name_display()


class TestSportLevelListView:
    def test_list(self, user: User) -> None:
        request = request_factory.get(
            reverse("participants:sport_levels"),
        )
        force_authenticate(request, user=user)
        response = SportLevelListView.as_view()(request)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["results"]
        for data, sport_level in zip(response.data["results"], SportLevel.objects.all()):
            assert data["value"] == sport_level.pk
            assert data["display"] == sport_level.get_level_display()


class TestPlayerSportCreateView:
    def test_create(self, user_without_sport: User) -> None:
        sport = random.choice(Sport.objects.all())
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "sport": sport.pk,
            "level": sport_level.pk,
        }
        request = request_factory.post(
            reverse("participants:player_sports"),
            data=data,
        )
        force_authenticate(request, user=user_without_sport)
        response = PlayerSportCreateView.as_view()(request)

        assert response.status_code == http_status.HTTP_201_CREATED
        assert response.data["sport"] == sport.pk
        assert response.data["level"] == sport_level.pk

    def test_create_when_has_same_sport(self, user: User) -> None:
        sport = user.player.sports.first().sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "sport": sport.pk,
            "level": sport_level.pk,
        }
        request = request_factory.post(
            reverse("participants:player_sports"),
            data=data,
        )
        force_authenticate(request, user=user)
        response = PlayerSportCreateView.as_view()(request)

        assert response.status_code == http_status.HTTP_400_BAD_REQUEST


class TestPlayerSportUpdateView:
    def test_update(self, user: User) -> None:
        sport_pk = user.player.sports.first().sport_id
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "level": sport_level.pk,
        }
        request = request_factory.put(
            reverse("participants:player_sports_update_level", kwargs={"sport_pk": sport_pk}),
            data=data,
        )
        force_authenticate(request, user=user)
        response = PlayerSportUpdateView.as_view()(request, sport_pk=sport_pk)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["sport"] == sport_pk
        assert response.data["level"] == sport_level.pk

    def test_update_when_player_does_not_have_sport(self, user_without_sport: User) -> None:
        sport_pk = random.choice(Sport.objects.all()).pk
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "level": sport_level.pk,
        }
        request = request_factory.put(
            reverse("participants:player_sports_update_level", kwargs={"sport_pk": sport_pk}),
            data=data,
        )
        force_authenticate(request, user=user_without_sport)
        response = PlayerSportUpdateView.as_view()(request, sport_pk=sport_pk)

        assert response.status_code == http_status.HTTP_404_NOT_FOUND

    def test_partial_update(self, user: User) -> None:
        sport_pk = user.player.sports.first().sport_id
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "level": sport_level.pk,
        }
        request = request_factory.patch(
            reverse("participants:player_sports_update_level", kwargs={"sport_pk": sport_pk}),
            data=data,
        )
        force_authenticate(request, user=user)
        response = PlayerSportUpdateView.as_view()(request, sport_pk=sport_pk)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["sport"] == sport_pk
        assert response.data["level"] == sport_level.pk

    def test_partial_update_when_player_does_not_have_sport(self, user_without_sport: User) -> None:
        sport_pk = random.choice(Sport.objects.all()).pk
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "level": sport_level.pk,
        }
        request = request_factory.patch(
            reverse("participants:player_sports_update_level", kwargs={"sport_pk": sport_pk}),
            data=data,
        )
        force_authenticate(request, user=user_without_sport)
        response = PlayerSportUpdateView.as_view()(request, sport_pk=sport_pk)

        assert response.status_code == http_status.HTTP_404_NOT_FOUND


class TestParticipationRequestCreateView:
    @pytest.mark.parametrize(
        "user, user2",
        [
            (
                {"player__sports__level_id": 1, "player_sports_size": 1, "player__sports__sport_id": 1},
                {"player__sports__level_id": 1, "player_sports_size": 1, "player__sports__sport_id": 1},
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
        force_authenticate(request, user=user2)
        response = ParticipationRequestCreateView.as_view()(request)

        assert response.status_code == http_status.HTTP_201_CREATED
        assert response.data["activity"] == activity_without_players.pk
        assert response.data["message"] == message
