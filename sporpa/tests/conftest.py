import pytest

from django.utils import timezone

from accounts.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        "testuser@example.com",
        "testpassword",
    )


@pytest.fixture
def passive_user() -> User:
    return User.objects.create_user(
        "passiveuser@example.com",
        "testpassword",
        deleted_at=timezone.now(),
    )
