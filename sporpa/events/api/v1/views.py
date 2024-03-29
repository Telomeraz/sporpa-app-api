from typing import Any, Type

from rest_framework import generics
from rest_framework import status as http_status
from rest_framework import views
from rest_framework.response import Response

from django.db.models import QuerySet

from events.models import Activity
from participants.models import ParticipationRequest

from .filtersets import ActivityListFilterset, ParticipatedActivityListFilterset
from .serializers import (
    ActivityCreateSerializer,
    ActivityListSerializer,
    ActivityUpdateSerializer,
    ParticipationRequestListSerializer,
)


class ActivityListCreateView(generics.ListCreateAPIView):
    filterset_class = ActivityListFilterset

    def get_serializer_class(self) -> Type[ActivityListSerializer | ActivityCreateSerializer]:
        if self.request.method == "GET":
            return ActivityListSerializer
        return ActivityCreateSerializer

    def get_queryset(self) -> QuerySet[Activity]:
        return Activity.objects.filter_available(self.request.user.player)


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


class ParticipationRequestApprovalView(views.APIView):
    def post(self, *args: Any, **kwargs: Any) -> Response:
        pk: int = kwargs["pk"]
        result: str = kwargs["result"]

        participation_request: ParticipationRequest = generics.get_object_or_404(
            ParticipationRequest.objects.filter_organizer(self.request.user.player),
            pk=pk,
        )
        if result == "accept":
            participation_request.activity.accept_participation_request(participation_request)
        else:
            participation_request.activity.reject_participation_request(participation_request)
        return Response({}, status=http_status.HTTP_204_NO_CONTENT)


class ParticipatedActivityListView(generics.ListAPIView):
    serializer_class = ActivityListSerializer
    filterset_class = ParticipatedActivityListFilterset

    def get_queryset(self) -> QuerySet[Activity]:
        return Activity.objects.filter(players=self.request.user.player)
