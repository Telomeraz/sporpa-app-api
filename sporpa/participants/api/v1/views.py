from typing import Any

from rest_framework import generics, request, response

from participants.models import Sport, SportLevel

from .serializers import PlayerSportSerializer, SportLevelSerializer, SportSerializer


class SportListView(generics.ListAPIView):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()


class SportLevelListView(generics.ListAPIView):
    serializer_class = SportLevelSerializer
    queryset = SportLevel.objects.all()


class PlayerSportCreateView(generics.CreateAPIView):
    serializer_class = PlayerSportSerializer

    def create(self, request: request.Request, *args: tuple, **kwargs: dict[str, Any]) -> response.Response:
        self.request.data["player"] = self.request.user.player
        return super().create(request, *args, **kwargs)
