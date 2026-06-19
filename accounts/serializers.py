from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "phone",
            "role",
        ]

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            role=validated_data["role"],
        )