import io
import tempfile

import pytest
from faker import Faker
from PIL import Image

from django.utils import timezone

from accounts.models import User
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def passive_user() -> User:
    return UserFactory(
        deleted_at=timezone.now(),
    )


@pytest.fixture
def image_file() -> tempfile._TemporaryFileWrapper:
    image = Image.open(io.BytesIO(fake.image()))
    tmp_file = tempfile.NamedTemporaryFile(suffix=f".{fake.file_extension('image')}")
    image.save(tmp_file)
    return tmp_file
