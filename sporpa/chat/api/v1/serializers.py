from rest_framework import serializers

from chat.models import ActivityMessage


class ActivityMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityMessage
        fields = (
            "pk",
            "sender",
            "activity",
            "created_at",
            "content",
        )
