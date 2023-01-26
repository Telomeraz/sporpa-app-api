import io
import tempfile

import pytest
from _pytest.fixtures import SubRequest
from faker import Faker
from PIL import Image

from accounts.models import User
from events.models import Activity
from tests.accounts.factories import UserFactory
from tests.events.factories import ActivityFactory

fake = Faker()
pytestmark = pytest.mark.django_db


@pytest.fixture
def user(request: SubRequest) -> User:
    data = getattr(request, "param", {})
    return UserFactory(**data)


@pytest.fixture
def user2(request: SubRequest) -> User:
    data = getattr(request, "param", {})
    return UserFactory(**data)


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
def activity_without_players(request: SubRequest, user: User) -> Activity:
    data = getattr(request, "param", {})
    return ActivityFactory(organizer=user.player, **data)


@pytest.fixture
def activity_with_participants(request: SubRequest, user: User) -> Activity:
    data = getattr(request, "param", {})
    total_participants = data.pop("total_participants", 1)
    activity: Activity = ActivityFactory(organizer=user.player, **data)
    for i in range(total_participants):
        activity.players.add(
            UserFactory(
                player__sports__level=activity.levels.first(),
                player_sports_size=1,
                player__sports__sport=activity.sport,
            ).player,
        )
    return activity
