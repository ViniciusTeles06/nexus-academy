from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "avatar",
            "is_email_verified",
        )

        read_only_fields = (
            "id",
            "email",
            "full_name",
            "role",
            "is_email_verified",
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "E-mail ou senha inválidos."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Esta conta está desativada."
            )

        attrs["user"] = user

        return attrs


class GoogleLoginSerializer(serializers.Serializer):
    credential = serializers.CharField(
        write_only=True,
        trim_whitespace=True,
    )

    def validate_credential(self, value):
        if not value:
            raise serializers.ValidationError(
                "A credencial do Google é obrigatória."
            )

        return value