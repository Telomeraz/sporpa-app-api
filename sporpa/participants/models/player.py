from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Player(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="player",
        limit_choices_to=models.Q(is_active=True),
        primary_key=True,
    )

    class Meta:
        db_table = "player"
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self) -> str:
        return f"{self.user}"
