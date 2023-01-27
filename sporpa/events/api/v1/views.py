from typing import Any

from rest_framework import generics
from rest_framework import status as http_status
from rest_framework import views
from rest_framework.response import Response

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


class ParticipationRequestApprovalView(views.APIView):
    def post(self, *args: Any, **kwargs: Any) -> Response:
        pk: int = kwargs["pk"]
        result: str = kwargs["result"]

        participation_request: ParticipationRequest = generics.get_object_or_404(
            ParticipationRequest.objects.filter_organizer(self.request.user.player),
            pk=pk,
        )
        if result == "accept":
            participation_request.activity.accept_participant_request(participation_request)
        else:
            participation_request.activity.reject_participant_request(participation_request)
        return Response({}, status=http_status.HTTP_204_NO_CONTENT)
