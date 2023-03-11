from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    content = models.TextField(
        _("content"),
        max_length=600,
        blank=True,
    )

    class Meta:
        abstract = True
