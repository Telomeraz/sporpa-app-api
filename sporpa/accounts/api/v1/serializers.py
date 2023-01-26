from rest_framework import serializers

from accounts.models import User
from participants.api.v1.serializers import PlayerSerializer


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "birthdate",
            "gender",
            "about",
            "player",
        )
