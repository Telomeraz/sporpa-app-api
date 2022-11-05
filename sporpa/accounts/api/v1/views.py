from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics

from accounts.api.v1.serializers import UserUpdateSerializer
from accounts.models import User


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
