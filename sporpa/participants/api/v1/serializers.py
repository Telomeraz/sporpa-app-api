from typing import Any

from rest_framework import serializers

from django.utils.translation import gettext

from events.models import Activity
from participants.models import ParticipationRequest, Player, PlayerSport, Sport, SportLevel

from .fields import CurrentPlayerDefault


class SportSerializer(serializers.ModelSerializer):
    value = serializers.ChoiceField(source="name", choices=Sport.Name)
    display = serializers.CharField(source="get_name_display")

    class Meta:
        model = Sport
        fields = (
            "value",
            "display",
        )


class SportLevelSerializer(serializers.ModelSerializer):
    value = serializers.ChoiceField(source="level", choices=SportLevel.Level)
    display = serializers.CharField(source="get_level_display")

    class Meta:
        model = SportLevel
        fields = (
            "value",
            "display",
        )


class PlayerSportSerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=CurrentPlayerDefault())

    class Meta:
        model = PlayerSport
        fields = (
            "player",
            "sport",
            "level",
        )
        extra_kwargs = {
            "write_only": {"player": True},
        }
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=PlayerSport.objects.all(),
                fields=("player", "sport"),
            ),
        )

    def create(self, validated_data: dict[str, Any]) -> PlayerSport:
        return validated_data["player"].create_sport(validated_data)


class PlayerSportUpdateSerializer(serializers.ModelSerializer):
    player = serializers.HiddenField(default=CurrentPlayerDefault())

    class Meta:
        model = PlayerSport
        fields = (
            "player",
            "sport",
            "level",
        )
        read_only_fields = ("sport",)
        extra_kwargs = {
            "write_only": {"player": True},
        }

    def update(self, instance: PlayerSport, validated_data: dict[str, Any]) -> PlayerSport:
        instance.update_level(validated_data["level"])
        return instance


class PlayerSerializer(serializers.ModelSerializer):
    sports = PlayerSportSerializer(many=True)

    class Meta:
        model = Player
        fields = (
            "pk",
            "sports",
        )


class ParticipationRequestListCreateSerializer(serializers.ModelSerializer):
    participant = serializers.HiddenField(default=CurrentPlayerDefault())

    class Meta:
        model = ParticipationRequest
        fields = (
            "activity",
            "participant",
            "created_at",
            "message",
        )
        extra_kwargs = {
            "write_only": {"participant": True},
            "read_only": {"created_at": True},
        }
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=ParticipationRequest.objects.all(),
                fields=("activity", "participant"),
                message=gettext("You already sent a participation request."),
            ),
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        validated_data = super().validate(attrs)
        participant: Player = validated_data["participant"]
        activity: Activity = validated_data["activity"]

        activity.check_participant(participant=participant)
        return validated_data
