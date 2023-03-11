from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .message import Message


class DirectMessage(Message):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("sender"),
        on_delete=models.CASCADE,
        related_name="sent_direct_messages",
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("receiver"),
        on_delete=models.CASCADE,
        related_name="received_direct_messages",
    )

    class Meta:
        db_table = "direct_message"
        verbose_name = _("direct message")
        verbose_name_plural = _("direct messages")

    def __str__(self) -> str:
        return f"Direct message from {self.sender} to {self.receiver}"
