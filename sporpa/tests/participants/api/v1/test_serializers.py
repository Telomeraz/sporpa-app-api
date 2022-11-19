import pytest

from participants.api.v1.serializers import SportSerializer
from participants.models import Sport

pytestmark = pytest.mark.django_db


class TestSportSerializer:
    def test_update(self) -> None:
        sport = Sport.objects.first()
        assert sport is not None
        data = {
            "value": sport.name,
            "display": sport.get_name_display(),
        }

        serializer = SportSerializer(sport)

        assert serializer.data == data
