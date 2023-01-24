from typing import Any

from drf_extra_fields.fields import DateTimeRangeField
from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from events.models import Activity
from events.validators import validate_now_less_than_lower_value
from participants.api.v1.fields import CurrentPlayerDefault
from participants.models import Player, PlayerSport, Sport, SportLevel


class ActivityCreateSerializer(serializers.ModelSerializer):
    organizer = serializers.HiddenField(
        default=CurrentPlayerDefault(),
        write_only=True,
    )
    available_between_at = DateTimeRangeField(
        # Model.validator doesn't work, bug in drf-extra-fields.
        validators=(validate_now_less_than_lower_value,),
    )

    class Meta:
        model = Activity
        fields = (
            "pk",
            "sport",
            "levels",
            "organizer",
            "player_limit",
            "name",
            "about",
            "available_between_at",
            "status",
        )
        extra_kwargs = {
            "levels": {
                "read_only": False,
                "queryset": SportLevel.objects.all(),
            },
            "status": {"read_only": True},
        }

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        validated_data = super().validate(attrs)
        organizer: Player = validated_data["organizer"]
        sport: Sport = validated_data["sport"]
        try:
            player_sport: PlayerSport = organizer.sports.get(sport=sport)
        except PlayerSport.DoesNotExist:
            raise serializers.ValidationError(
                _(f"The player does not have {sport.get_name_display()} record."),
            )

        sport_levels: list[SportLevel] = validated_data["levels"]
        if player_sport.level not in sport_levels:
            raise serializers.ValidationError(
                _(f"The player does not have the requested level for {sport.get_name_display()}."),
            )
        return validated_data


class ActivityUpdateSerializer(serializers.ModelSerializer):
    available_between_at = DateTimeRangeField(
        validators=(validate_now_less_than_lower_value,),
    )

    class Meta:
        model = Activity
        fields = (
            "pk",
            "sport",
            "levels",
            "players",
            "player_limit",
            "name",
            "about",
            "available_between_at",
            "status",
        )
        extra_kwargs = {
            "sport": {"read_only": True},
            "levels": {"read_only": True},
            "players": {"read_only": True},
        }

    def validate_player_limit(self, value: int) -> int:
        self.instance.check_player_limit(player_limit=value)
        return value
