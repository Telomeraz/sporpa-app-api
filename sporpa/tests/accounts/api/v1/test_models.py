import pytest
from faker import Faker

from accounts.models import User, user_directory_path
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user(self) -> None:
        user = User.objects.create_user(email=fake.email(), password=fake.password())
        assert user.pk is not None
        assert user.is_active is True
        assert User.objects.count() == 1
        assert user.auth_token.key

    def test_create_user_when_empty_email(self) -> None:
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password=fake.password())
            assert True

    def test_create_superuser(self) -> None:
        user = User.objects.create_superuser(email=fake.email(), password=fake.password())
        assert user.pk is not None
        assert user.is_active is True
        assert user.is_superuser is True
        assert User.objects.count() == 1

    def test_create_superuser_when_is_superuser_true(self) -> None:
        user = User.objects.create_superuser(email=fake.email(), password=fake.password(), is_superuser=True)
        assert user.pk is not None
        assert user.is_active is True
        assert user.is_superuser is True
        assert User.objects.count() == 1

    def test_create_superuser_when_is_superuser_false(self) -> None:
        with pytest.raises(ValueError):
            User.objects.create_superuser(email=fake.email(), password=fake.password(), is_superuser=False)
            assert True


@pytest.mark.parametrize("filename", [fake.file_name("image")])
def test_user_directory_path(user: User, filename: str) -> None:
    path = user_directory_path(user, filename)
    assert path == f"avatars/user/{user.email}/{filename}"


class TestUser:
    def test_clean(self, user: User) -> None:
        user.email = "testuser@EXAMPLE.COM"
        user.clean()
        assert user.email == "testuser@example.com"

    def test_full_name(self) -> None:
        user: User = UserFactory.build(
            email=fake.email(),
            password=fake.password(),
            first_name="Adam",
            last_name="Smith",
        )
        assert user.full_name == "Adam Smith"
