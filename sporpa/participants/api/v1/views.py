from rest_framework import generics

from django.db.models import QuerySet

from participants.models import ParticipationRequest, PlayerSport, Sport, SportLevel

from .serializers import (
    ParticipationRequestListCreateSerializer,
    PlayerSportSerializer,
    PlayerSportUpdateSerializer,
    SportLevelSerializer,
    SportSerializer,
)


class SportListView(generics.ListAPIView):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()


class SportLevelListView(generics.ListAPIView):
    serializer_class = SportLevelSerializer
    queryset = SportLevel.objects.all()


class PlayerSportCreateView(generics.CreateAPIView):
    serializer_class = PlayerSportSerializer


class PlayerSportUpdateView(generics.UpdateAPIView):
    serializer_class = PlayerSportUpdateSerializer
    lookup_field = "sport_pk"

    def get_object(self) -> PlayerSport:
        player = self.request.user.player
        sport_pk = self.kwargs[self.lookup_field]
        return generics.get_object_or_404(player.sports, sport=sport_pk)


class ParticipationRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ParticipationRequestListCreateSerializer

    def get_queryset(self) -> QuerySet[ParticipationRequest]:
        return ParticipationRequest.objects.filter_participant(self.request.user.player)
