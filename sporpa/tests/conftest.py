import io
import tempfile

import pytest
from faker import Faker
from PIL import Image

from accounts.models import User
from events.models import Activity
from tests.accounts.factories import UserFactory
from tests.events.factories import ActivityFactory

fake = Faker()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def user2() -> User:
    return UserFactory()


@pytest.fixture
def user_without_sport() -> User:
    return UserFactory(player=None)


@pytest.fixture
def unverified_user() -> User:
    return UserFactory(email_address1__verified=False)


@pytest.fixture
def image_file() -> tempfile._TemporaryFileWrapper:
    image = Image.open(io.BytesIO(fake.image()))
    tmp_file = tempfile.NamedTemporaryFile(suffix=f".{fake.file_extension('image')}")
    image.save(tmp_file)
    return tmp_file


@pytest.fixture
def activity_without_players(user: User) -> Activity:
    return ActivityFactory(organizer=user.player)
