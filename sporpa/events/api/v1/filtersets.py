from django_filters import rest_framework as filters

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from events.models import Activity
from participants.models import Sport


class BaseActivityListFilterset(filters.FilterSet):
    sport = filters.ModelMultipleChoiceFilter(
        field_name="sport",
        queryset=Sport.objects.all(),
    )
    available_between_at = filters.DateTimeFromToRangeFilter(
        "available_between_at",
        method="_filter_available_between_at",
    )

    def _filter_available_between_at(
        self,
        queryset: QuerySet[Activity],
        name: str,
        value: slice,
    ) -> QuerySet[Activity]:
        if value.start:
            queryset = queryset.filter(available_between_at__gt=(value.start, None))
        if value.stop:
            queryset = queryset.filter(available_between_at__lt=(value.stop, None))
        return queryset


class ActivityListFilterset(BaseActivityListFilterset):
    class Meta:
        model = Activity
        fields = (
            "sport",
            "levels",
            "available_between_at",
        )


class ParticipatedActivityListFilterset(BaseActivityListFilterset):
    PT_ORGANIZER = "organizer"
    PT_PARTICIPANT = "participant"
    PLAYER_TYPES = (
        (PT_ORGANIZER, _("Organizer")),
        (PT_PARTICIPANT, _("Participant")),
    )

    status = filters.TypedMultipleChoiceFilter(
        field_name="status",
        choices=Activity.Status.choices,
        coerce=int,
    )
    player_type = filters.TypedChoiceFilter(
        method="_filter_player_type",
        choices=PLAYER_TYPES,
        coerce=str,
    )

    class Meta:
        model = Activity
        fields = (
            "sport",
            "levels",
            "available_between_at",
            "status",
            "player_type",
        )

    def _filter_player_type(
        self,
        queryset: QuerySet[Activity],
        name: str,
        value: str,
    ) -> QuerySet[Activity]:
        if value == self.PT_ORGANIZER:
            queryset = queryset.filter_organizer(self.request.user.player)
        elif value == self.PT_PARTICIPANT:
            queryset = queryset.filter_participant(self.request.user.player)
        return queryset
