from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class SignupSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'nickname', 'password', 'full_name', 'phone_number', 'auth_number']

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
