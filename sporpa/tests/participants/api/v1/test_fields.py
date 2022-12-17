import pytest
from rest_framework import fields
from rest_framework.test import APIRequestFactory

from django.urls import reverse

from accounts.models import User
from participants.api.v1.fields import CurrentPlayerDefault

pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


class TestCurrentPlayerDefault:
    def test_call(self, user: User) -> None:
        request = request_factory.get(
            reverse("participants:sports"),
        )
        request.user = user
        context = {
            "request": request,
        }
        field = fields.Field(default=CurrentPlayerDefault())
        field._context = context
        default = field.get_default()

        assert default == user.player

    def test_repr(self) -> None:
        assert repr(CurrentPlayerDefault()) == "CurrentPlayerDefault()"
