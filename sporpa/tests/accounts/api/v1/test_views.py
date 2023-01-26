import tempfile

import pytest
from faker import Faker
from rest_framework import status as http_status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse
from django.utils.dateparse import parse_date

from accounts.api.v1.views import UserRetrieveUpdateView
from accounts.models import User

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestUserRetrieveUpdateView:
    def test_retrieve(self, user: User, user2: User) -> None:
        request = request_factory.get(
            reverse("accounts-users", kwargs={"pk": user2.pk}),
        )
        force_authenticate(request, user=user)
        response = UserRetrieveUpdateView.as_view()(request, pk=user2.pk)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["first_name"] == user2.first_name
        assert response.data["last_name"] == user2.last_name
        assert response.data["avatar"] == request.build_absolute_uri(user2.avatar.url)
        assert parse_date(response.data["birthdate"]) == user2.birthdate
        assert response.data["gender"] == user2.gender
        assert response.data["about"] == user2.about
        for data, player_sport in zip(response.data["player"]["sports"], user2.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id

    def test_update(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
        password = fake.password()
        with open(image_file.name, "rb") as image_data:
            data = {
                "email": fake.email(),
                "password": password,
                "password2": password,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "avatar": image_data,
                "birthdate": fake.date_of_birth(),
                "about": fake.text(max_nb_chars=User.about.field.max_length),
            }
            request = request_factory.put(
                reverse("accounts-users"),
                data=data,
                format="multipart",
            )
        force_authenticate(request, user=user)
        response = UserRetrieveUpdateView.as_view()(request)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
        assert response.data["avatar"] == request.build_absolute_uri(user.avatar.url)
        assert parse_date(response.data["birthdate"]) == user.birthdate
        assert response.data["gender"] == user.gender
        assert response.data["about"] == user.about
        for data, player_sport in zip(response.data["player"]["sports"], user.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id

    def test_partial_update(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
        with open(image_file.name, "rb") as image_data:
            data = {
                "avatar": image_data,
                "birthdate": fake.date_of_birth(),
                "about": fake.text(max_nb_chars=User.about.field.max_length),
            }
            request = request_factory.patch(
                reverse("accounts-users"),
                data=data,
                format="multipart",
            )
        force_authenticate(request, user=user)
        response = UserRetrieveUpdateView.as_view()(request)

        assert response.status_code == http_status.HTTP_200_OK
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name
        assert response.data["avatar"] == request.build_absolute_uri(user.avatar.url)
        assert parse_date(response.data["birthdate"]) == user.birthdate
        assert response.data["gender"] == user.gender
        assert response.data["about"] == user.about
        for data, player_sport in zip(response.data["player"]["sports"], user.player.sports.all()):
            assert data["sport"] == player_sport.sport_id
            assert data["level"] == player_sport.level_id
