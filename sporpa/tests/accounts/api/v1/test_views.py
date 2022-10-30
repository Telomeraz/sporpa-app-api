import tempfile

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from django.urls import reverse

from accounts.api.v1.views import UserUpdateView
from accounts.models import User

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestUserUpdateView:
    def test_put(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
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
                reverse("user_update"),
                data=data,
            )
        force_authenticate(request, user=user)
        response = UserUpdateView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK

    def test_patch(self, user: User, image_file: tempfile._TemporaryFileWrapper) -> None:
        with open(image_file.name, "rb") as image_data:
            data = {
                "avatar": image_data,
                "birthdate": fake.date_of_birth(),
                "about": fake.text(max_nb_chars=User.about.field.max_length),
            }
            request = request_factory.patch(
                reverse("user_update"),
                data=data,
            )
        force_authenticate(request, user=user)
        response = UserUpdateView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
