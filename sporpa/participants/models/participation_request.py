from django.db import models
from django.utils.translation import gettext_lazy as _


class ParticipationRequest(models.Model):
    activity = models.ForeignKey(
        "events.Activity",
        verbose_name=_("activity"),
        on_delete=models.CASCADE,
        related_name="participation_requests",
    )
    participant = models.ForeignKey(
        "participants.Player",
        verbose_name=_("participant"),
        on_delete=models.CASCADE,
        related_name="participation_requests",
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    message = models.CharField(
        _("message"),
        max_length=250,
        blank=True,
    )

    class Meta:
        db_table = "participation_request"
        verbose_name = _("participation request")
        verbose_name_plural = _("participation requests")

    def __str__(self) -> str:
        return f"{self.participant}'s participation request"
