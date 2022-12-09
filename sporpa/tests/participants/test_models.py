import random

import pytest

from django.db import IntegrityError

from accounts.models import User
from participants.models import PlayerSport, Sport, SportLevel

pytestmark = pytest.mark.django_db


class TestSport:
    def test_str(self) -> None:
        sport = random.choice(Sport.objects.all())
        assert str(sport) == sport.get_name_display()


class TestSportLevel:
    def test_str(self) -> None:
        sport_level = random.choice(SportLevel.objects.all())
        assert str(sport_level) == sport_level.get_level_display()


class TestPlayerSportManager:
    def test_filter_player(self, user: User) -> None:
        player_sports = PlayerSport.objects.filter_player(user.player)
        assert player_sports.count() == PlayerSport.objects.filter(player=user.player).count()
        for player_sport in player_sports:
            assert player_sport.player == user.player

    def test_filter_player_when_send_int_as_parameter(self, user: User) -> None:
        player_sports = PlayerSport.objects.filter_player(user.player.pk)
        assert player_sports.count() == PlayerSport.objects.filter(player=user.player).count()
        for player_sport in player_sports:
            assert player_sport.player == user.player

    def test_filter_player_when_player_does_not_have_sport(self, user_without_sport: User) -> None:
        player_sports = PlayerSport.objects.filter_player(user_without_sport.player)
        assert player_sports.count() == PlayerSport.objects.filter(player=user_without_sport.player).count()


class TestPlayerSport:
    def test_str(self, user_without_sport: User) -> None:
        sport = random.choice(Sport.objects.all())
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user_without_sport.player,
            "sport": sport,
            "level": sport_level,
        }
        player_sport = user_without_sport.player.create_sport(data)
        assert str(player_sport) == f"{player_sport.player} - {player_sport.sport} - {player_sport.level}"

    def test_update_level(self, user: User) -> None:
        sport = user.player.sports.first()
        sport_level = random.choice(SportLevel.objects.all())
        sport.update_level(sport_level)

        assert sport.level == sport_level


class TestPlayer:
    def test_create_sport(self, user_without_sport: User) -> None:
        sport = random.choice(Sport.objects.all())
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user_without_sport.player,
            "sport": sport,
            "level": sport_level,
        }

        player_sport = user_without_sport.player.create_sport(data)

        assert user_without_sport.player.sports.filter(pk=player_sport.pk).exists()

    def test_create_sport_when_has_same_sport(self, user: User) -> None:
        sport = user.player.sports.first().sport
        sport_level = random.choice(SportLevel.objects.all())
        data = {
            "player": user.player,
            "sport": sport,
            "level": sport_level,
        }

        with pytest.raises(IntegrityError):
            user.player.create_sport(data)
