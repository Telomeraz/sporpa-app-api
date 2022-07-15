import pytest
from faker import Faker

from accounts.models import User, user_directory_path

fake = Faker()
pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user(self) -> None:
        user = User.objects.create_user(email=fake.email(), password=fake.password())
        assert user.pk is not None
        assert user.is_active is True
        assert User.objects.count() == 1

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
    assert path == f"avatars/user_{user.pk}/{filename}"
