from typing import Any

from rest_framework import generics, request, response

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

    def create(self, request: request.Request, *args: tuple, **kwargs: dict[str, Any]) -> response.Response:
        self.request.data["player"] = self.request.user.player
        return super().create(request, *args, **kwargs)


class PlayerSportUpdateLevelView(generics.UpdateAPIView):
    serializer_class = PlayerSportUpdateLevelSerializer
    lookup_field = "sport_id"

    def get_object(self) -> PlayerSport:
        player = self.request.user.player
        sport_id = self.kwargs[self.lookup_field]
        return generics.get_object_or_404(player.sports, sport=sport_id)

    def update(self, request: request.Request, *args: tuple, **kwargs: dict[str, Any]) -> response.Response:
        self.request.data["player"] = self.request.user.player
        return super().update(request, *args, **kwargs)
