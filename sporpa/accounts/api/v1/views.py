from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics

from accounts.api.v1.serializers import UserSerializer
from accounts.models import User


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class UserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.select_related("player").prefetch_related(
        "player__sports",
    )

    def get_object(self) -> User:
        if self.request.method == "GET":
            return super().get_object()
        return self.request.user
