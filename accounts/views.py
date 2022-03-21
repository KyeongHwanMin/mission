from django.contrib.auth import login, logout
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import models
from accounts.models import User
from accounts.serializers import SignupSerializer, MyinfoSerializer, ChangePasswordSerializer


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
        email = serializer.validated_data['email']
        phone_number = serializer.validated_data['phone_number']
        nickname = serializer.validated_data['nickname']
        auth_number = serializer.validated_data['auth_number']

        if User.objects.filter(username=username).exists():
            return Response(data={'error': '이미 존재하는 계정 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response(data={'error': '이미 존재하는 이메일 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response(data={'error': '이미 존재하는 핸드폰 번호 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(nickname=nickname).exists():
            return Response(data={'error': '이미 존재하는 닉네임 입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        if models.Auth.objects.filter(phone_number=phone_number).exists():
            user_auth_number = models.Auth.objects.get(phone_number=phone_number).auth_number
            if auth_number == user_auth_number:
                User.objects.create_user(username=username, email=email, nickname=nickname,
                                         password=serializer.validated_data['password'],
                                         full_name=serializer.validated_data['full_name'],
                                         phone_number=phone_number, auth_number=auth_number)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'error': '인증번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': '인증 되어 있지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


def login_by_uesrname(username, password):
    user = None
    try:
        user = User.objects.get(username=username)
        user.check_password(password)
        is_success = True
    except User.DoesNotExist:
        is_success = False

    return user, is_success


def login_by_email(email, password):
    user = None
    try:
        user = User.objects.get(email=email)
        user.check_password(password)
        is_success = True
    except User.DoesNotExist:
        is_success = False

    return user, is_success


def login_by_nickname(nickname, password):
    user = None
    try:
        user = User.objects.get(nickname=nickname)
        user.check_password(password)
        is_success = True
    except User.DoesNotExist:
        is_success = False

    return user, is_success


def login_by_phone_number(phone_number, password):
    user = None
    try:
        user = User.objects.get(phone_number=phone_number)
        user.check_password(password)
        is_success = True
    except User.DoesNotExist:
        is_success = False

    return user, is_success


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        nickname = request.data.get('nickname')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        password = request.data.get('password')

        user, is_success = login_by_uesrname(username, password)
        if not is_success:
            user, is_success = login_by_nickname(nickname, password)
        if not is_success:
            user, is_success = login_by_phone_number(phone_number, password)
        if not is_success:
            user, is_success = login_by_email(email, password)
        if not is_success:
            return Response(data={'error': '아이디 혹은 비밀번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response(data={'success': '로그인 완료'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class MyinfoView(APIView):
    def get(self, request):
        qs = User.objects.filter(username=request.user)
        serializer = MyinfoSerializer(qs, many=True)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

