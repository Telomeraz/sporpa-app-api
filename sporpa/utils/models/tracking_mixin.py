from typing import Any

from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class TrackingManagerMixin(models.Manager):
    def __init__(self, *args: tuple, **kwargs: Any) -> None:
        self.all_objects = kwargs.pop("all_objects", False)
        super().__init__(*args, **kwargs)

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.all_objects:
            return queryset
        return queryset.filter(is_active=True)


class TrackingMixin(models.Model):
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this record should be treated as active. " "Unselect this instead of deleting records."
        ),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        help_text=_(
            "Enter a datetime instead when you delete the record.",
        ),
        null=True,
        blank=True,
    )

    objects = TrackingManagerMixin()
    all_objects = TrackingManagerMixin(all_objects=True)

    class Meta:
        abstract = True
