from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from accounts.api.v1.serializers import AuthTokenSerializer, UserCreateSerializer, UserUpdateSerializer
from accounts.models import User


class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = UserCreateSerializer


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self) -> User:
        return self.request.user
