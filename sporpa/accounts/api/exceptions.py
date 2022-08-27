from rest_framework import status
from rest_framework.exceptions import APIException

from django.utils.translation import gettext_lazy as _


class NotVerifiedEmail(APIException):
    """
    The user has not verified email.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Please verify your email address.")
    default_code = "email_verification"


class AlreadyVerifiedEmail(APIException):
    """
    The user has already verified email.
    """

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("User has already verified email.")
    default_code = "already_verified"


class InvalidToken(APIException):
    """
    The token is invalid or expired.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Token is invalid or expired.")
    default_code = "invalid_token"
