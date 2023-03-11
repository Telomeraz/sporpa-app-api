from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .message import Message


class ActivityMessage(Message):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("sender"),
        on_delete=models.CASCADE,
        related_name="sent_activity_messages",
    )
    activity = models.ForeignKey(
        "events.Activity",
        verbose_name=_("activity"),
        on_delete=models.CASCADE,
        related_name="messages",
    )

    class Meta:
        db_table = "activity_message"
        verbose_name = _("activity message")
        verbose_name_plural = _("activity messages")

    def __str__(self) -> str:
        return f"Activity message from {self.sender} to {self.activity}"
