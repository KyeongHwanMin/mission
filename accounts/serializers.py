from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class SignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'password', 'full_name', 'phone_number', 'auth_number']


class MyinfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'nickname',
            'full_name',
            'phone_number',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    auth_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
