from typing import Any

from rest_framework.authtoken.models import Token

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TrackingManagerMixin, TrackingMixin


class UserManager(BaseUserManager, TrackingManagerMixin):
    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_directory_path(instance: "User", filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/user_<pk>/<filename>
    return f"avatars/user/{instance.email}/{filename}"


class User(AbstractBaseUser, PermissionsMixin, TrackingMixin):
    class Gender(models.IntegerChoices):
        UNSPECIFIED = 0, _("Unspecified")
        MALE = 1, _("Male")
        FEMALE = 2, _("Female")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: list = []
    username = None
    auth_token: Token

    first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    has_verified_email = models.BooleanField(
        _("verified email"),
        default=False,
        help_text=_(
            "Designates whether this user has verified email address.",
        ),
    )
    avatar = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
    )
    birthdate = models.DateField(
        _("birthdate"),
        null=True,
    )
    gender = models.PositiveSmallIntegerField(
        _("gender"),
        choices=Gender.choices,
        default=Gender.UNSPECIFIED,
    )
    about = models.TextField(
        _("about"),
        max_length=600,
        blank=True,
    )

    objects: UserManager = UserManager()
    all_objects = UserManager(all_objects=True)

    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def send_verification_email(self, url: str) -> int:
        subject = _("Sporpa Email Verification")
        message = _(
            f"Hi {self.full_name},\n\nYou can verify your email address by clicking on the link below:\n\n"
            f"{self.generate_email_verification_address(url=url)}\n\n"
            "Thank you,\nThe Sporpa Team"
        )
        return self.email_user(subject, message, from_email="Sporpa")

    def email_user(self, subject: str, message: str, from_email: str | None = None, **kwargs: Any) -> int:
        return send_mail(subject, message, from_email, [self.email], **kwargs)

    def generate_email_verification_address(self, url: str) -> str:
        token = self.make_token()
        return f"{url}?token={token}"

    def make_token(self) -> str:
        return default_token_generator.make_token(self)

    def check_token(self, token: str) -> bool:
        return default_token_generator.check_token(self, token)

    def verify_email(self) -> None:
        self.has_verified_email = True
        self.save()
