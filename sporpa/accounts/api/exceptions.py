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
