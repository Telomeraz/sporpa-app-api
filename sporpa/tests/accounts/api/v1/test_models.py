import pytest
from faker import Faker
from rest_framework.test import APIRequestFactory

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import User, user_directory_path
from tests.accounts.factories import UserFactory

fake = Faker()
pytestmark = pytest.mark.django_db
request_factory = APIRequestFactory()


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

    def test_send_verification_email(self, user: User) -> None:
        build_absolute_uri = request_factory.get(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": user.email},
            ),
        ).build_absolute_uri
        url = build_absolute_uri(
            reverse(
                "api.v1.accounts:verify-email",
                kwargs={"email": user.email},
            ),
        )
        token = user.make_token()

        subject = _("Sporpa Email Verification")
        message = _(
            f"Hi {user.full_name},\n\nYou can verify your email address by clicking on the link below:\n\n"
            f"{url}?token={token}\n\n"
            "Thank you,\nThe Sporpa Team"
        )
        user.send_verification_email(build_absolute_uri=build_absolute_uri)
        assert len(mail.outbox) == 1
        assert subject == mail.outbox[0].subject
        assert message == mail.outbox[0].body

    def test_email_user(self, user: User) -> None:
        subject = _("Test Subject")
        message = _("Test Message")
        num_sent = user.email_user(subject=subject, message=message)
        assert num_sent == 1
        assert subject == mail.outbox[0].subject
        assert message == mail.outbox[0].body

    def test_generate_token_link(self, user: User) -> None:
        fake_url = fake.url()
        url = user.generate_token_link(fake_url)
        assert url == f"{fake_url}?token={user.make_token()}"

    def test_make_token(self, user: User) -> None:
        token = user.make_token()
        assert token == default_token_generator.make_token(user)

    def test_check_token(self, user: User) -> None:
        token = user.make_token()
        assert user.check_token(token) is True

    def test_verify_email(self, unverified_user: User) -> None:
        unverified_user.verify_email()
        assert unverified_user.has_verified_email is True
