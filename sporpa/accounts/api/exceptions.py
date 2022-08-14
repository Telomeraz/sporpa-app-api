from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


class NotVerifiedEmail(ValidationError):
    """
    The user has not verified email.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Please verify your email address.")
    default_code = "email_verification"
