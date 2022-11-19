import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from participants.api.v1.serializers import SportSerializer
from participants.api.v1.views import SportListView
from participants.models import Sport

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestSportListView:
    def test_get(self, user: User) -> None:
        request = request_factory.get(
            reverse("sport_list"),
        )
        force_authenticate(request, user=user)
        response = SportListView.as_view()(request)

        sports = Sport.objects.all()
        serializer = SportSerializer(sports, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        assert response.data["results"] == serializer.data
