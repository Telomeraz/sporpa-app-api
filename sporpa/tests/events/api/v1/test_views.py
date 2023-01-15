import random

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from events.api.v1.views import ActivityUpdateView, ActivityView
from events.models import Activity
from participants.models import PlayerSport, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestActivityView:
    def test_create(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels: set[SportLevel] = set(
            random.sample(
                list(SportLevel.objects.values_list(flat=True)),
                k=random.randint(0, SportLevel.objects.count()),
            ),
        )
        sport_levels.add(player_sport.level.pk)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="+1d", end_date="+15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }

        data = {
            "name": name,
            "about": about,
            "sport": sport.pk,
            "levels": sport_levels,
            "available_between_at": available_between_at,
        }
        request = request_factory.post(
            reverse("events:activities"),
            data=data,
        )
        force_authenticate(request, user=user)
        response = ActivityView.as_view()(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["pk"]
        assert response.data["sport"] == sport.pk
        assert response.data["levels"] == list(sport_levels)
        assert response.data["player_limit"] == Activity.player_limit.field.default
        assert response.data["name"] == name
        assert response.data["about"] == about
        assert response.data["status"] == Activity.status.field.default

    def test_create_when_user_does_not_have_sport(self, user_without_sport: User) -> None:
        sport: Sport = Sport.objects.first()
        sport_levels = SportLevel.objects.values_list(flat=True)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="+1d", end_date="+15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }

        data = {
            "name": name,
            "about": about,
            "sport": sport.pk,
            "levels": sport_levels,
            "available_between_at": available_between_at,
        }
        request = request_factory.post(
            reverse("events:activities"),
            data=data,
        )
        force_authenticate(request, user=user_without_sport)
        response = ActivityView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_when_user_does_not_have_sport_level(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels = SportLevel.objects.exclude(pk=player_sport.level.pk).values_list(flat=True)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="+1d", end_date="+15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }

        data = {
            "name": name,
            "about": about,
            "sport": sport.pk,
            "levels": sport_levels,
            "available_between_at": available_between_at,
        }
        request = request_factory.post(
            reverse("events:activities"),
            data=data,
        )
        force_authenticate(request, user=user)
        response = ActivityView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_when_lower_value_less_than_now(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels = (player_sport.level.pk,)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="-1d", end_date="-15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }

        data = {
            "name": name,
            "about": about,
            "sport": sport.pk,
            "levels": sport_levels,
            "available_between_at": available_between_at,
        }
        request = request_factory.post(
            reverse("events:activities"),
            data=data,
        )
        force_authenticate(request, user=user)
        response = ActivityView.as_view()(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestActivityUpdateView:
    def test_update(self, activity: Activity) -> None:
        player_limit = random.randint(
            Activity.player_limit.field.validators[0].limit_value,
            Activity.player_limit.field.validators[1].limit_value,
        )
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="+1d", end_date="+15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }
        status_ = random.choice(Activity.Status.values)

        data = {
            "player_limit": player_limit,
            "name": name,
            "about": about,
            "available_between_at": available_between_at,
            "status": status_,
        }
        request = request_factory.put(
            reverse("events:activities_update", kwargs={"pk": activity.pk}),
            data=data,
        )
        force_authenticate(request, user=activity.organizer.user)
        response = ActivityUpdateView.as_view()(request, pk=activity.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["player_limit"] == player_limit
        assert response.data["name"] == name
        assert response.data["about"] == about
        assert response.data["status"] == status_

    def test_partial_update(self, activity: Activity) -> None:
        player_limit = random.randint(
            Activity.player_limit.field.validators[0].limit_value,
            Activity.player_limit.field.validators[1].limit_value,
        )
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = {
            "lower": fake.date_time_between(start_date="+1d", end_date="+15d"),
            "upper": fake.date_time_between(start_date="+16d", end_date="+30d"),
        }
        status_ = random.choice(Activity.Status.values)

        data = {
            "player_limit": player_limit,
            "name": name,
            "about": about,
            "available_between_at": available_between_at,
            "status": status_,
        }
        request = request_factory.patch(
            reverse("events:activities_update", kwargs={"pk": activity.pk}),
            data=data,
        )
        force_authenticate(request, user=activity.organizer.user)
        response = ActivityUpdateView.as_view()(request, pk=activity.pk)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["player_limit"] == player_limit
        assert response.data["name"] == name
        assert response.data["about"] == about
        assert response.data["status"] == status_
