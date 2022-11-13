from django.db import models
from django.utils.translation import gettext_lazy as _


class Sport(models.Model):
    class Name(models.IntegerChoices):
        FOOTBALL = 1, _("Football")
        BASKETBALL = 2, _("Basketball")
        VOLLEYBALL = 3, _("Volleyball")
        TENIS = 4, _("Tennis")
        TABLE_TENNIS = 5, _("Table Tennis")

    name = models.PositiveSmallIntegerField(
        _("name"),
        choices=Name.choices,
        primary_key=True,
    )

    class Meta:
        db_table = "sport"
        verbose_name = _("sport")
        verbose_name_plural = _("sports")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.get_name_display()
