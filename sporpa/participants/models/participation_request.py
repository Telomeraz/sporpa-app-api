from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from participants import models as participants_models


class ParticipationRequestManager(models.Manager):
    def filter_participant(self, participant: "participants_models.Player | int") -> models.QuerySet:
        return self.filter(participant=participant)

    def filter_organizer(self, organizer: "participants_models.Player | int") -> models.QuerySet:
        return self.filter(
            activity__activity_players__is_organizer=True,
            activity__players=organizer,
        )


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

    objects = ParticipationRequestManager()

    class Meta:
        db_table = "participation_request"
        verbose_name = _("participation request")
        verbose_name_plural = _("participation requests")
        constraints = (
            models.UniqueConstraint(
                fields=("activity", "participant"),
                name="activity_participant_unique",
                violation_error_message=gettext("You already sent a participation request."),
            ),
        )

    def __str__(self) -> str:
        return f"{self.participant}'s participation request"
