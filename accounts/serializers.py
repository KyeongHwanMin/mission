from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
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


class ChangePasswordSerializer(ModelSerializer):
    auth_number = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['auth_number', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return data

    def update(self, instance, validated_data):
        user_auth_number = validated_data.get('user_auth_number', instance.auth_number)
        auth_number = int(validated_data.get('auth_number'))

        if user_auth_number == auth_number:
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'auth_number': '인증번호가 일치하지 않습니다.'})
