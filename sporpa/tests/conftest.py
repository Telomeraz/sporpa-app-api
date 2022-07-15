import pytest

from django.utils import timezone

from accounts.models import User
from tests.accounts.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def passive_user() -> User:
    return UserFactory(
        deleted_at=timezone.now(),
    )
