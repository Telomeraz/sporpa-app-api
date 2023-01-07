from rest_framework import generics

from .serializers import ActivitySerializer


class ActivityView(generics.CreateAPIView):
    serializer_class = ActivitySerializer
