from rest_framework import generics

from django.db.models import QuerySet

from events.models import Activity
from participants.models import ParticipationRequest

from .serializers import ActivityCreateSerializer, ActivityUpdateSerializer, ParticipationRequestListSerializer


class ActivityCreateView(generics.CreateAPIView):
    serializer_class = ActivityCreateSerializer


class ActivityUpdateView(generics.UpdateAPIView):
    serializer_class = ActivityUpdateSerializer

    def get_queryset(self) -> QuerySet[Activity]:
        return Activity.objects.filter_organizer(self.request.user.player).filter(
            status__in=Activity.UPDATABLE_STATUSES,
        )


class ParticipationRequestListView(generics.ListAPIView):
    serializer_class = ParticipationRequestListSerializer
    lookup_field = "activity_pk"

    def get_queryset(self) -> QuerySet[Activity]:
        activity_pk = self.kwargs[self.lookup_field]
        return ParticipationRequest.objects.filter_organizer(self.request.user.player).filter(
            activity=activity_pk,
        )
