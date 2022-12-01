import random

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from participants.api.v1.views import PlayerSportCreateView, SportLevelListView, SportListView
from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestSportListView:
    def test_get(self, user: User) -> None:
        request = request_factory.get(
            reverse("sport_list"),
        )
        force_authenticate(request, user=user)
        response = SportListView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport in zip(response.data["results"], Sport.objects.all()):
            assert data["value"] == sport.pk
            assert data["display"] == sport.get_name_display()


class TestSportLevelListView:
    def test_get(self, user: User) -> None:
        request = request_factory.get(
            reverse("sport_level_list"),
        )
        force_authenticate(request, user=user)
        response = SportLevelListView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport_level in zip(response.data["results"], SportLevel.objects.all()):
            assert data["value"] == sport_level.pk
            assert data["display"] == sport_level.get_level_display()


class TestPlayerSportCreateView:
    def test_post(self, user_without_sport: User) -> None:
        sport = random.choice(Sport.objects.all())
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "sport": sport.pk,
            "level": sport_level.pk,
        }
        request = request_factory.post(
            reverse("player_sport_create"),
            data=data,
        )
        force_authenticate(request, user=user_without_sport)
        response = PlayerSportCreateView.as_view()(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["sport"] == sport.pk
        assert response.data["level"] == sport_level.pk

    def test_post_when_has_same_sport(self, user: User) -> None:
        sport = user.player.sports.first().sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "sport": sport.pk,
            "level": sport_level.pk,
        }
        request = request_factory.post(
            reverse("player_sport_create"),
            data=data,
        )
        force_authenticate(request, user=user)
        response = PlayerSportCreateView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
