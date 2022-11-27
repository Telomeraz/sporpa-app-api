import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.models import User
from participants.api.v1.views import SportLevelListView, SportListView
from participants.models import Sport, SportLevel

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestSportListView:
    def test_get(self, user: User) -> None:
        request = request_factory.get(
            reverse("sport_list"),
        )
        force_authenticate(request, user=user)
        response = SportListView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport in zip(response.data["results"], Sport.objects.all()):
            assert data["value"] == sport.pk
            assert data["display"] == sport.get_name_display()


class TestSportLevelListView:
    def test_get(self, user: User) -> None:
        request = request_factory.get(
            reverse("sport_level_list"),
        )
        force_authenticate(request, user=user)
        response = SportLevelListView.as_view()(request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"]
        for data, sport_level in zip(response.data["results"], SportLevel.objects.all()):
            assert data["value"] == sport_level.pk
            assert data["display"] == sport_level.get_level_display()
