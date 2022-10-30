from rest_framework import serializers

from accounts.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "birthdate",
            "gender",
            "about",
        )
