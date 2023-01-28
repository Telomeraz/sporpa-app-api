import random

import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.models import User
from events.api.v1.serializers import (
    ActivityCreateSerializer,
    ActivityUpdateSerializer,
    ParticipatedActivityListSerializer,
    ParticipationRequestListSerializer,
)
from events.models import Activity
from participants.models import ParticipationRequest, PlayerSport, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestActivityCreateSerializer:
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
        serializer = ActivityCreateSerializer(data=data, context=context)
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
        serializer = ActivityCreateSerializer(data=data, context=context)
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
        serializer = ActivityCreateSerializer(data=data, context=context)
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
        serializer = ActivityCreateSerializer(data=data, context=context)
        assert serializer.is_valid() is False


class TestActivityUpdateSerializer:
    def test_update(self, activity_without_participants: Activity) -> None:
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
        status = random.choice(Activity.Status.values)

        data = {
            "player_limit": player_limit,
            "name": name,
            "about": about,
            "available_between_at": available_between_at,
            "status": status,
        }
        serializer = ActivityUpdateSerializer(instance=activity_without_participants, data=data)
        assert serializer.is_valid()

        updated_activity_without_participants: Activity = serializer.save()

        assert updated_activity_without_participants.player_limit == player_limit
        assert updated_activity_without_participants.name == name
        assert updated_activity_without_participants.about == about
        assert updated_activity_without_participants.available_between_at.lower == available_between_at["lower"]
        assert updated_activity_without_participants.available_between_at.upper == available_between_at["upper"]
        assert updated_activity_without_participants.status == status

    def test_partial_update(self, activity_without_participants: Activity) -> None:
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
        status = random.choice(Activity.Status.values)

        data = {
            "player_limit": player_limit,
            "name": name,
            "about": about,
            "available_between_at": available_between_at,
            "status": status,
        }
        serializer = ActivityUpdateSerializer(instance=activity_without_participants, data=data, partial=True)
        assert serializer.is_valid()

        updated_activity_without_participants: Activity = serializer.save()

        assert updated_activity_without_participants.player_limit == player_limit
        assert updated_activity_without_participants.name == name
        assert updated_activity_without_participants.about == about
        assert updated_activity_without_participants.available_between_at.lower == available_between_at["lower"]
        assert updated_activity_without_participants.available_between_at.upper == available_between_at["upper"]
        assert updated_activity_without_participants.status == status


class TestParticipationRequestListSerializer:
    def test_data(self, participation_request: ParticipationRequest) -> None:
        serializer = ParticipationRequestListSerializer(participation_request)

        assert serializer.data["participant"]["pk"] == participation_request.participant.pk
        assert serializer.data["message"] == participation_request.message
        for data, participant_sport in zip(
            serializer.data["participant"]["sports"],
            participation_request.participant.sports.all(),
        ):
            assert data["sport"] == participant_sport.sport.pk
            assert data["level"] == participant_sport.level.pk


class TestParticipatedActivityListSerializer:
    def test_data(self, activity_with_participants: Activity) -> None:
        activity_with_participants.refresh_from_db()
        serializer = ParticipatedActivityListSerializer(activity_with_participants)

        organizer = activity_with_participants.organizer
        participants = activity_with_participants.participants

        assert serializer.data["pk"] == activity_with_participants.pk
        assert serializer.data["sport"] == activity_with_participants.sport.pk
        assert serializer.data["levels"] == list(activity_with_participants.levels.values_list("pk", flat=True))

        assert serializer.data["organizer"]["pk"] == organizer.pk
        assert serializer.data["organizer"]["user"]["first_name"] == organizer.user.first_name
        assert serializer.data["organizer"]["user"]["last_name"] == organizer.user.last_name

        for data_, participant in zip(
            serializer.data["participants"],
            participants,
        ):
            assert data_["pk"] == participant.pk
            assert data_["user"]["first_name"] == participant.user.first_name
            assert data_["user"]["last_name"] == participant.user.last_name

        assert serializer.data["player_limit"] == activity_with_participants.player_limit
        assert serializer.data["name"] == activity_with_participants.name
        assert serializer.data["about"] == activity_with_participants.about
        assert serializer.data["status"] == activity_with_participants.status
