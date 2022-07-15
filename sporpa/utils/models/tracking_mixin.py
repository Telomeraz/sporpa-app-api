from typing import Any, Optional, Tuple

from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class TrackingManagerMixin(models.Manager):
    def __init__(self, *args: Tuple, **kwargs: Optional[Any]) -> None:
        self.all_objects = kwargs.pop("all_objects", False)
        super().__init__(*args, **kwargs)

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.all_objects:
            return queryset
        return queryset.filter(deleted_at__isnull=True)


class TrackingMixin(models.Model):
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        default=None,
        help_text=_(
            "Designates whether this user should be treated as active. Enter a datetime instead of deleting user.",
        ),
        null=True,
        blank=True,
    )

    objects = TrackingManagerMixin()
    all_objects = TrackingManagerMixin(all_objects=True)

    class Meta:
        abstract = True
