from typing import Any

from django.contrib.postgres.fields import DateTimeRangeField
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from events.validators import validate_now_less_than_lower_value
from participants.models import Player
from utils.models import TrackingManagerMixin, TrackingMixin


class ActivityManager(TrackingManagerMixin):
    def create(self, **kwargs: Any) -> "Activity":
        organizer: Player = kwargs.pop("organizer")
        activity: Activity = super().create(**kwargs)
        activity.players.add(organizer, through_defaults={"is_organizer": True})
        return activity

    def filter_organizer(self, organizer: Player | int) -> models.QuerySet:
        return self.filter(
            activity_players__is_organizer=True,
            players=organizer,
        )


class Activity(TrackingMixin):
    class Status(models.IntegerChoices):
        OPEN = 1, _("Open")
        PLAYED = 2, _("Played")
        CANCELLED = 3, _("Cancelled")

    UPDATABLE_STATUSES = (Status.OPEN,)

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
    players = models.ManyToManyField(
        "participants.Player",
        verbose_name=_("player"),
        related_name="activities",
        through="events.ActivityPlayer",
        through_fields=("activity", "player"),
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
        validators=(validate_now_less_than_lower_value,),
    )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=Status.choices,
        default=Status.OPEN,
    )

    objects = ActivityManager()

    class Meta:
        db_table = "activity"
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
        constraints = (
            models.CheckConstraint(
                check=models.Q(available_between_at__lower_inf=False),
                name="lower_cannot_be_infinite",
                violation_error_message=_("available_between_at lower value cannot be infinite."),
            ),
            models.CheckConstraint(
                check=models.Q(available_between_at__upper_inf=False),
                name="upper_cannot_be_infinite",
                violation_error_message=_("available_between_at upper value cannot be infinite."),
            ),
        )

    def __str__(self) -> str:
        return self.name

    @property
    def organizer(self) -> Player:
        return self.players.get(activity_players__is_organizer=True)

    def check_player_limit(
        self,
        *,
        player_limit: int | None = None,
        total_players: int | None = None,
    ) -> None:
        player_limit = player_limit if player_limit is not None else self.player_limit
        total_players = total_players if total_players is not None else len(self.players.all())

        if player_limit < total_players:
            raise ValidationError(_("Player limit cannot be less than total players."))
