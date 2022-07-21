from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView

from .serializers import AuthTokenSerializer, UserSerializer


class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class RegisterView(CreateAPIView):
    permission_classes = ()
    serializer_class = UserSerializer
