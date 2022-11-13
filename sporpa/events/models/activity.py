from django.contrib.postgres.fields import DateTimeRangeField
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import TrackingMixin


class Activity(TrackingMixin):
    class Status(models.IntegerChoices):
        OPEN = 1, _("Open")
        PLAYED = 2, _("Played")
        CANCELLED = 3, _("Cancelled")

    sport = models.ForeignKey(
        "participants.Sport",
        verbose_name=_("sport"),
        on_delete=models.PROTECT,
        related_name="activities",
    )
    levels = models.ManyToManyField(
        "participants.SportLevel",
        verbose_name=_("level"),
        related_name="activities",
        through="events.ActivityLevel",
        through_fields=("activity", "level"),
    )
    player_sports = models.ManyToManyField(
        "participants.PlayerSport",
        verbose_name=_("player sport"),
        related_name="activities",
        through="events.ActivityPlayer",
        through_fields=("activity", "player_sport"),
    )
    player_limit = models.PositiveSmallIntegerField(
        _("maximum number of players"),
        default=2,
        validators=(
            validators.MinValueValidator(2),
            validators.MaxValueValidator(30),
        ),
    )
    name = models.CharField(
        _("name"),
        max_length=150,
    )
    about = models.TextField(
        _("about"),
        max_length=600,
        blank=True,
    )
    available_between_at = DateTimeRangeField(
        _("available between at"),
    )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=Status.choices,
        default=Status.OPEN,
    )

    class Meta:
        db_table = "activity"
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self) -> str:
        return self.name
