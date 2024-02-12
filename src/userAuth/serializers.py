from rest_framework import serializers
from .models import CustomUser


class UserSignUpSerializer(serializers.ModelSerializer):

    con_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'con_password']

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("con_password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.pop("username", instance.username)
        instance.email = validated_data.pop("email", instance.email)

        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=50)


class TokenLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    token = serializers.CharField(max_length=100)