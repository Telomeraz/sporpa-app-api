from rest_framework import generics, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.request import Request
from rest_framework.views import Response

from django.utils.translation import gettext as _

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


class SendEmailVerificationView(views.APIView):
    permission_classes = ()

    def post(self, request: Request, email: str) -> Response:
        user: User = generics.get_object_or_404(User, email=email)

        if user.has_verified_email:
            return Response({"detail": _("User has already verified email")}, status=status.HTTP_409_CONFLICT)

        user.send_email_verification(build_absolute_uri=request.build_absolute_uri)
        return Response({"detail": _("Email verification sent.")})


class VerifyEmailView(views.APIView):
    permission_classes = ()

    def post(self, request: Request, email: str) -> Response:
        user: User = generics.get_object_or_404(User, email=email)
        token = request.query_params.get("token")

        if user.has_verified_email:
            return Response({"detail": _("User has already verified email")}, status=status.HTTP_409_CONFLICT)

        if not user.check_token(token):
            return Response({"detail": _("Token is invalid or expired.")}, status=status.HTTP_400_BAD_REQUEST)

        user.verify_email()
        return Response({"detail": _("Email verified.")})
