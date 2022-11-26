from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import generics

from accounts.api.v1.serializers import UserSerializer
from accounts.models import User


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
