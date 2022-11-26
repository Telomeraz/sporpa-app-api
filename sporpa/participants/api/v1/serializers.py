from rest_framework import serializers

from participants.models import Player, PlayerSport, Sport, SportLevel


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
    sport = SportSerializer(read_only=True)
    level = SportLevelSerializer()

    class Meta:
        model = PlayerSport
        fields = (
            "sport",
            "level",
        )


class PlayerSerializer(serializers.ModelSerializer):
    sports = PlayerSportSerializer(many=True)

    class Meta:
        model = Player
        fields = ("sports",)
