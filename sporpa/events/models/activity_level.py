from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityLevel(models.Model):
    activity = models.ForeignKey(
        "events.Activity",
        verbose_name=_("activity"),
        on_delete=models.CASCADE,
        related_name="activity_levels",
    )
    level = models.ForeignKey(
        "participants.SportLevel",
        verbose_name=_("level"),
        on_delete=models.CASCADE,
        related_name="activity_levels",
    )

    class Meta:
        db_table = "activity_level"
        verbose_name = _("activity level")
        verbose_name_plural = _("activity levels")
        constraints = (
            models.UniqueConstraint(
                fields=("activity", "level"),
                name="activity_level_unique",
            ),
        )

    def __str__(self) -> str:
        return f"{self.activity} - {self.level}"
