from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import AuthTokenSerializer


class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
