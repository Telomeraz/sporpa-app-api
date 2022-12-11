from rest_framework import generics

from participants.models import PlayerSport, Sport, SportLevel

from .serializers import PlayerSportSerializer, PlayerSportUpdateLevelSerializer, SportLevelSerializer, SportSerializer


class SportView(generics.ListAPIView):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()


class SportLevelView(generics.ListAPIView):
    serializer_class = SportLevelSerializer
    queryset = SportLevel.objects.all()


class PlayerSportView(generics.CreateAPIView):
    serializer_class = PlayerSportSerializer


class PlayerSportUpdateLevelView(generics.UpdateAPIView):
    serializer_class = PlayerSportUpdateLevelSerializer
    lookup_field = "sport_id"

    def get_object(self) -> PlayerSport:
        player = self.request.user.player
        sport_id = self.kwargs[self.lookup_field]
        return generics.get_object_or_404(player.sports, sport=sport_id)
