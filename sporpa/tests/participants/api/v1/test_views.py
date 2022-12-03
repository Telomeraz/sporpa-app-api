import random

import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from participants.api.v1.views import PlayerSportView, SportLevelView, SportView
from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestSportView:
    def test_list(self, user: User) -> None:
        request = request_factory.get(
            reverse("participants:sports"),
        )
        force_authenticate(request, user=user)
        response = SportView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport in zip(response.data["results"], Sport.objects.all()):
            assert data["value"] == sport.pk
            assert data["display"] == sport.get_name_display()


class TestSportLevelView:
    def test_list(self, user: User) -> None:
        request = request_factory.get(
            reverse("participants:sport_levels"),
        )
        force_authenticate(request, user=user)
        response = SportLevelView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport_level in zip(response.data["results"], SportLevel.objects.all()):
            assert data["value"] == sport_level.pk
            assert data["display"] == sport_level.get_level_display()


class TestPlayerSportView:
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
        response = PlayerSportView.as_view()(request)

        assert response.status_code == status.HTTP_201_CREATED
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
        response = PlayerSportView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
