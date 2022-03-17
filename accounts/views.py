from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import models
from accounts.models import User
from accounts.serializers import SignupSerializer


class Auth(APIView):
    def post(self, request):
        try:
            phone_number = request.data['phone_number']

        except KeyError:
            return Response({'message': 'Bad Request'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            models.Auth.objects.update_or_create(phone_number=phone_number)
            auth_number = models.Auth.objects.filter(phone_number=phone_number).values('auth_number')
            return Response(auth_number)


class Signupview(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        phone_number = serializer.validated_data['phone_number']
        auth_number = serializer.validated_data['auth_number']

        if User.objects.filter(username=username).exists():
            return Response(data={'error': '이미 존재하는 계정입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_auth_number = models.Auth.objects.get(phone_number=phone_number)
        if auth_number == user_auth_number.auth_number:
            User.objects.create_user(username=username, email=serializer.validated_data['email'],
                                     nickname=serializer.validated_data['nickname'],
                                     password=serializer.validated_data['password'],
                                     full_name=serializer.validated_data['full_name'],
                                     phone_number=phone_number, auth_number=auth_number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'error': '인증번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
