from django.db import models
from django.utils.translation import gettext_lazy as _


class SportLevel(models.Model):
    class Level(models.IntegerChoices):
        BEGINNER = 1, _("Beginner")
        LOWER_INTERMEDIATE = 2, _("Lower Intermediate")
        INTERMEDIATE = 3, _("Intermediate")
        UPPER_INTERMEDIATE = 4, _("Upper Intermediate")
        EXPERT = 5, _("Expert")

    level = models.PositiveSmallIntegerField(
        _("level"),
        choices=Level.choices,
        primary_key=True,
    )

    class Meta:
        db_table = "sport_level"
        verbose_name = _("sport level")
        verbose_name_plural = _("sport levels")
        ordering = ("level",)

    def __str__(self) -> str:
        return self.get_level_display()
