from rest_framework import exceptions
from rest_framework import status as http_status
from rest_framework.response import Response
from rest_framework.views import set_rollback

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404


def exception_handler(exc: Exception, context: dict) -> Response:
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"detail": exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    if isinstance(exc, ValidationError):
        if isinstance(exc.message, (list, dict)):
            data = exc.message
        else:
            data = {"detail": exc.message}

        set_rollback()
        return Response(data, status=exc.code or http_status.HTTP_400_BAD_REQUEST)
    return None
