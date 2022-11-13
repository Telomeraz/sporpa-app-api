from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityPlayer(models.Model):
    activity = models.ForeignKey(
        "events.Activity",
        verbose_name=_("activity"),
        on_delete=models.CASCADE,
    )
    player_sport = models.ForeignKey(
        "participants.PlayerSport",
        verbose_name=_("player"),
        on_delete=models.CASCADE,
    )
    is_organizer = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "activity_player"
        verbose_name = _("activity player")
        verbose_name_plural = _("activity players")
        constraints = (
            models.UniqueConstraint(
                fields=("activity", "is_organizer"),
                condition=models.Q(is_organizer=True),
                name="only_one_organizer",
            ),
        )

    def __str__(self) -> str:
        return f"{self.activity} - {self.player_sport}"
