from typing import Any, List

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
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
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
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
    return f"avatars/user_{instance.pk}/{filename}"


class User(AbstractBaseUser, PermissionsMixin, TrackingMixin):
    class Gender(models.IntegerChoices):
        UNSPECIFIED = 0, _("Unspecified")
        MALE = 1, _("Male")
        FEMALE = 2, _("Female")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: List = []
    username = None

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

    objects = UserManager()
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

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str = None,
        **kwargs: Any,
    ) -> None:
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
