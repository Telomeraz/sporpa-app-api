import random

import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.models import User
from events.api.v1.serializers import ActivitySerializer
from events.models import Activity
from participants.models import PlayerSport, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestActivitySerializer:
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
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = ActivitySerializer(data=data, context=context)
        assert serializer.is_valid()

        activity: Activity = serializer.save()

        assert activity.pk
        assert activity.sport == sport
        assert list(activity.levels.values_list(flat=True)) == list(sport_levels)
        assert activity.player_limit == Activity.player_limit.field.default
        assert activity.name == name
        assert activity.about == about
        assert activity.available_between_at.lower == available_between_at["lower"]
        assert activity.available_between_at.upper == available_between_at["upper"]
        assert activity.status == Activity.status.field.default

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
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user_without_sport
        context = {
            "request": request,
        }
        serializer = ActivitySerializer(data=data, context=context)
        assert serializer.is_valid() is False

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
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = ActivitySerializer(data=data, context=context)
        assert serializer.is_valid() is False

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
            reverse("participants:player_sports"),
            data=data,
        )
        request.user = user
        context = {
            "request": request,
        }
        serializer = ActivitySerializer(data=data, context=context)
        assert serializer.is_valid() is False
