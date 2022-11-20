import pytest

from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db


class TestSport:
    def test__str__(self) -> None:
        sport = Sport.objects.get(name=Sport.Name.FOOTBALL.value)
        assert str(sport) == Sport.Name.FOOTBALL.label


class TestSportLevel:
    def test__str__(self) -> None:
        sport_level = SportLevel.objects.get(level=SportLevel.Level.BEGINNER.value)
        assert str(sport_level) == SportLevel.Level.BEGINNER.label
