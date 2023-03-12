import functools
from typing import Callable

from channels.sessions import CookieMiddleware
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware:
    def __init__(self, inner: CookieMiddleware) -> None:
        self.inner = inner

    async def __call__(
        self,
        scope: dict,
        receive: Callable,
        send: functools.partial,
    ) -> CookieMiddleware:
        headers = dict(scope.get("headers", {}))
        if b"authorization" in headers:
            try:
                token_name, token_key = headers[b"authorization"].decode().split()
                if token_name == "Token":
                    token = await Token.objects.select_related("user__player").aget(key=token_key)
                    scope["user"] = token.user
            except Token.DoesNotExist:
                pass
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner: CookieMiddleware) -> TokenAuthMiddleware:
    return TokenAuthMiddleware(inner)
