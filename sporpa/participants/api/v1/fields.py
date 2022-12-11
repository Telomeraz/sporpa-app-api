from rest_framework import serializers

from participants.models import Player


class CurrentPlayerDefault:
    """
    A default class that can be used to represent the current player.
    In order to use this, the 'request' must have been provided as part of
    the context dictionary when instantiating the serializer.
    """

    requires_context = True

    def __call__(self, serializer_field: serializers.Field) -> Player:
        return serializer_field.context["request"].user.player

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
