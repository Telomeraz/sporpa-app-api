from django_filters import rest_framework as filters

from django.db.models import QuerySet

from events.models import Activity
from participants.models import Sport


class ActivityListFilterset(filters.FilterSet):
    sport = filters.ModelMultipleChoiceFilter(
        field_name="sport",
        queryset=Sport.objects.all(),
    )
    available_between_at = filters.DateTimeFromToRangeFilter(
        "available_between_at",
        method="_filter_available_between_at",
    )
    status = filters.TypedMultipleChoiceFilter(
        field_name="status",
        choices=Activity.Status.choices,
        coerce=int,
    )

    class Meta:
        model = Activity
        fields = (
            "sport",
            "levels",
            "available_between_at",
            "status",
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
