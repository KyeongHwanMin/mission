from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# User = get_user_model()
from accounts.models import User


class SignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'nickname', 'password', 'full_name', 'phone_number', 'auth_number']


class LoginSerializer(ModelSerializer):

    # username = serializers.CharField(read_only=True, required=False)
    # email = serializers.CharField(read_only=True, required=False)
    # phone_number = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']



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

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"current_password": "기존 비밀번호가 틀립니다."})
        return value

    def update(self, instance, validated_data):
        user_auth_number = validated_data.get('user_auth_number', instance.auth_number)
        auth_number = int(validated_data.get('auth_number'))

        if user_auth_number == auth_number:
            instance.set_password(validated_data['password'])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'auth_number': '인증번호가 일치하지 않습니다.'})

# class SignupSerializer(serializers.Modelserializer):
#     password = serializers.CharField(write_only=True)
#
#     def create(self, validated_data):
#         email = User.objects.create(emali=validated_data['email'])
#         user = User.objects.create(full_name=validated_data['full_name'])
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'nickname', 'password', 'full_name', 'phone_number']

# 회원가입
# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["username", "email", "password"]
#         extra_kwargs = {"password": {"write_only": True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data["username"], validated_data["email"], validated_data["password"]
#         )
#         return user
#
#
# # 로그인
# class LoginUserSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=64)
#     password = serializers.CharField()
#
#     def validate(self, data):
#         email = data.get("email", None)
#         password = data.get("password", None)
#         user = authenticate(email=email, password=password)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Unable to log in with provided credentials.")
