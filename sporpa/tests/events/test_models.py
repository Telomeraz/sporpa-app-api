import random

import pytest
from faker import Faker

from accounts.models import User
from events.models import Activity
from participants.models import Player, PlayerSport, Sport, SportLevel

fake = Faker()
pytestmark = pytest.mark.django_db


class TestActivityManager:
    def test_create(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels: set[SportLevel] = set(
            random.sample(
                list(SportLevel.objects.all()),
                k=random.randint(0, SportLevel.objects.count()),
            ),
        )
        sport_levels.add(player_sport.level)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = (
            fake.date_time_between(start_date="+1d", end_date="+15d"),
            fake.date_time_between(start_date="+16d", end_date="+30d"),
        )

        data = {
            "organizer": user.player,
            "name": name,
            "about": about,
            "sport": sport,
            "available_between_at": available_between_at,
        }
        activity = Activity.objects.create(**data)
        activity.levels.set(sport_levels)

        assert activity.pk
        assert activity.players.get(activity_players__is_organizer=True) == user.player
        assert activity.name == name
        assert activity.about == about
        assert activity.sport == sport
        assert list(activity.levels.all()) == list(sport_levels)
        assert activity.available_between_at == available_between_at
        assert Activity.objects.count() == 1

    def test_create_when_activity_does_not_have_organizer(self, user: User) -> None:
        player_sport: PlayerSport = user.player.sports.first()
        sport: Sport = player_sport.sport
        sport_levels: set[SportLevel] = set(
            random.sample(
                list(SportLevel.objects.all()),
                k=random.randint(0, SportLevel.objects.count()),
            ),
        )
        sport_levels.add(player_sport.level)
        name = fake.text(max_nb_chars=Activity.name.field.max_length)
        about = fake.text(max_nb_chars=Activity.about.field.max_length)
        available_between_at = (
            fake.date_time_between(start_date="+1d", end_date="+15d"),
            fake.date_time_between(start_date="+16d", end_date="+30d"),
        )

        data = {
            "name": name,
            "about": about,
            "sport": sport,
            "available_between_at": available_between_at,
        }
        with pytest.raises(KeyError):
            Activity.objects.create(**data)


class TestActivity:
    def test_str(self, activity_without_players: Activity) -> None:
        assert str(activity_without_players) == activity_without_players.name

    def test_organizer(self, activity_without_players: Activity) -> None:
        assert activity_without_players.organizer == Player.objects.get(
            activity_players__is_organizer=True,
            activities=activity_without_players,
        )
