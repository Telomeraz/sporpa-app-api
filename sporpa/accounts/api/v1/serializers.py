from typing import Dict, OrderedDict

from rest_framework import serializers

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True,
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        email = attrs["email"]
        password = attrs["password"]
        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        label=_("Password (again)"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "avatar",
            "birthdate",
            "gender",
            "about",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if attrs["password"] != attrs["password2"]:
            msg = _("Passwords do not match.")
            raise serializers.ValidationError(msg, code="invalid")
        del attrs["password2"]
        return super().validate(attrs)

    def create(self, validated_data: Dict) -> User:
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        label=_("Old Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )
    password2 = serializers.CharField(
        label=_("Password (again)"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            "old_password",
            "password",
            "password2",
            "first_name",
            "last_name",
            "avatar",
            "birthdate",
            "gender",
            "about",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        old_password = attrs.pop("old_password", None)
        password = attrs.get("password", None)
        password2 = attrs.pop("password2", None)
        if old_password and password and password2:
            if not self.instance.check_password(old_password):
                msg = _("Password is not valid.")
                raise serializers.ValidationError(msg, code="invalid")
            if password != password2:
                msg = _("Passwords do not match.")
                raise serializers.ValidationError(msg, code="invalid")
        else:
            attrs.pop("password", None)
        return super().validate(attrs)

    def update(self, instance: User, validated_data: Dict) -> User:
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
            del validated_data["password"]
        return super().update(instance, validated_data)
