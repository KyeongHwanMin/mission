from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, Auth
from accounts.permission import IsOwner
from accounts.serializers import SignupSerializer, MyinfoSerializer, ChangePasswordSerializer


class AuthView(APIView):
    def post(self, request):
        try:
            phone_number = request.data['phone_number']
        except KeyError:
            return Response({'error': 'phone_number를 입력해 주세요.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(str(phone_number)) != 11:
            return Response({'error': '11자리 혹은 -를 빼고 입력해주세요.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif int(phone_number[0]) != 0:
            return Response({'error': '올바른 전화번호를 입력해주세요.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            Auth.objects.update_or_create(phone_number=phone_number)
            auth_number = Auth.objects.filter(phone_number=phone_number).values('auth_number')
            return Response(auth_number)


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        nickname = serializer.validated_data['nickname']
        full_name = serializer.validated_data['full_name']
        phone_number = serializer.validated_data['phone_number']
        auth_number = int(request.data.get('auth_number'))

        if User.objects.filter(username=username).exists():
            return Response(data={'error': '이미 존재하는 계정 입니다.'}, status=status.HTTP_409_CONFLICT)
        if User.objects.filter(email=email).exists():
            return Response(data={'error': '이미 존재하는 이메일 입니다.'}, status=status.HTTP_409_CONFLICT)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response(data={'error': '이미 존재하는 핸드폰 번호 입니다.'}, status=status.HTTP_409_CONFLICT)
        if User.objects.filter(nickname=nickname).exists():
            return Response(data={'error': '이미 존재하는 닉네임 입니다.'}, status=status.HTTP_409_CONFLICT)

        try:
            user_auth_number = Auth.objects.get(phone_number=phone_number)
            if auth_number == user_auth_number.auth_number:
                User.objects.create_user(username=username, email=email, nickname=nickname,
                                         password=serializer.validated_data['password'], full_name=full_name,
                                         phone_number=phone_number)
                Auth.objects.get(phone_number=phone_number).delete()
                return Response(data={'success': '회원가입 완료'}, status=201)
            else:
                return Response(data={'error': '인증번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)

        except Auth.DoesNotExist:
            return Response(data={'error': '휴대폰 인증을 하세요.'}, status=status.HTTP_400_BAD_REQUEST)


def login_by_uesrname(username, password):
    user = None
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            is_success = True
        else:
            is_success = False
    except User.DoesNotExist:
        is_success = False

    return user, is_success


def login_by_email(email, password):
    user = None
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            is_success = True
        else:
            is_success = False
    except User.DoesNotExist:
        is_success = None

    return user, is_success


def login_by_nickname(nickname, password):
    user = None
    try:
        user = User.objects.get(nickname=nickname)
        if user.check_password(password):
            is_success = True
        else:
            is_success = False
    except User.DoesNotExist:
        is_success = False

    return user, is_success


def login_by_phone_number(phone_number, password):
    user = None
    try:
        user = User.objects.get(phone_number=phone_number)
        if user.check_password(password):
            is_success = True
        else:
            is_success = False
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
        if is_success is None:
            return Response(data={'error': '없는 계정입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not is_success:
            return Response(data={'error': '아이디 혹은 비밀번호가 틀립니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(data={'success': '로그인 완료'}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class MyinfoView(APIView):
    permission_classes = [IsOwner]

    def get_object(self, pk):
        try:
            qs = User.objects.get(pk=pk)
            self.check_object_permissions(self.request, qs)
            return qs
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        qs = self.get_object(pk)
        serializer = MyinfoSerializer(qs, context={'request': request})
        return Response(serializer.data)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        auth_number = int(serializer.validated_data['auth_number'])
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']
        try:

            auth = Auth.objects.get(auth_number=auth_number)

            if auth_number == auth.auth_number and phone_number == auth.phone_number:

                if password == password2:
                    user = User.objects.get(phone_number=auth.phone_number)
                    user.set_password(password)
                    Auth.objects.get(phone_number=phone_number).delete()
                    return Response(data={'success': '비밀번호 초기화 완료'}, status=status.HTTP_200_OK)

                else:
                    return Response(data={'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data={'error': '휴대폰 번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        except Auth.DoesNotExist:
            return Response(data={'error': '인증번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
