from rest_framework import generics

from django.db.models import QuerySet

from events.models import Activity

from .serializers import ActivitySerializer, ActivityUpdateSerializer


class ActivityView(generics.CreateAPIView):
    serializer_class = ActivitySerializer


class ActivityUpdateView(generics.UpdateAPIView):
    serializer_class = ActivityUpdateSerializer

    def get_queryset(self) -> QuerySet[Activity]:
        return Activity.objects.filter_organizer(self.request.user.player).filter(
            status__in=Activity.UPDATABLE_STATUSES,
        )
