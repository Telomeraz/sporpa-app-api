from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
        extra_kwargs = {
            "birthdate": {
                "required": True,
            },
        }


class TokenSerializer(serializers.ModelSerializer):
    is_profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = (
            "key",
            "is_profile_complete",
        )

    def get_is_profile_complete(self, obj: Token) -> bool:
        return obj.user.is_profile_complete
