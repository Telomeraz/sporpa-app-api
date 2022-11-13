from django.db import models
from django.utils.translation import gettext_lazy as _


class PlayerSport(models.Model):
    player = models.ForeignKey(
        "participants.Player",
        verbose_name=_("player"),
        on_delete=models.CASCADE,
        related_name="sports",
    )
    sport = models.ForeignKey(
        "participants.Sport",
        verbose_name=_("sport"),
        on_delete=models.PROTECT,
        related_name="player_sports",
    )
    level = models.ForeignKey(
        "participants.SportLevel",
        verbose_name=_("level"),
        on_delete=models.PROTECT,
        related_name="player_sports",
    )

    class Meta:
        db_table = "player_sport"
        verbose_name = _("player sport")
        verbose_name_plural = _("player sports")
        constraints = (
            models.UniqueConstraint(
                fields=("player", "sport"),
                name="player_sport_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.player.user} - {self.sport} - {self.level}"
