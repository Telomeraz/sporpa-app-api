import pytest

from participants.models import Sport

pytestmark = pytest.mark.django_db


class TestSport:
    def test__str__(self) -> None:
        sport = Sport.objects.get(name=Sport.Name.FOOTBALL.value)
        assert str(sport) == Sport.Name.FOOTBALL.label
