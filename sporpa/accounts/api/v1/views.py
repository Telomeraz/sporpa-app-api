from rest_framework import generics

from accounts.api.v1.serializers import UserUpdateSerializer
from accounts.models import User


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self) -> User:
        return self.request.user
