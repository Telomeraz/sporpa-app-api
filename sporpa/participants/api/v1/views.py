from rest_framework import generics

from participants.models import Sport

from .serializers import SportSerializer


class SportListView(generics.ListAPIView):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
