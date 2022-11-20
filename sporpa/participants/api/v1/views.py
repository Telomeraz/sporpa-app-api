from rest_framework import generics

from participants.models import Sport, SportLevel

from .serializers import SportLevelSerializer, SportSerializer


class SportListView(generics.ListAPIView):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()


class SportLevelListView(generics.ListAPIView):
    serializer_class = SportLevelSerializer
    queryset = SportLevel.objects.all()
