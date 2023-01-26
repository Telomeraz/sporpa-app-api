from rest_framework import generics

from participants.models import PlayerSport, Sport, SportLevel

from .serializers import (
    ParticipationRequestCreateSerializer,
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


class ParticipationRequestCreateView(generics.CreateAPIView):
    serializer_class = ParticipationRequestCreateSerializer
