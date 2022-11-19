from rest_framework import serializers

from participants.models import Sport


class SportSerializer(serializers.ModelSerializer):
    value = serializers.ChoiceField(source="name", choices=Sport.Name)
    display = serializers.CharField(source="get_name_display")

    class Meta:
        model = Sport
        fields = (
            "value",
            "display",
        )
