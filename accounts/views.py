from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts import models
from accounts.models import User
from accounts.serializers import SignupSerializer, MyinfoSerializer, ChangePasswordSerializer, LoginSerializer


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
        nickname = serializer.validated_data['nickname']
        auth_number = serializer.validated_data['auth_number']

        if User.objects.filter(username=username).exists():
            return Response(data={'error': '이미 존재하는 계정 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response(data={'error': '이미 존재하는 핸드폰 번호 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(nickname=nickname).exists():
            return Response(data={'error': '이미 존재하는 닉네임 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        if models.Auth.objects.filter(phone_number=phone_number).exists():
            user_auth_number = models.Auth.objects.get(phone_number=phone_number).auth_number
            if auth_number == user_auth_number:
                User.objects.create_user(username=username, email=serializer.validated_data['email'],
                                         nickname=nickname,
                                         password=serializer.validated_data['password'],
                                         full_name=serializer.validated_data['full_name'],
                                         phone_number=phone_number, auth_number=auth_number)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'error': '인증번호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': '인증 되어 있지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginView(APIView):
    def post(self, request):

        if request.data['password'] is None:
            return Response(data={'error': '비밀번호를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.data['username']:
            username = request.data['username']
            user = User.objects.filter(username=username)
            if user is None:
                return Response(data={'error': '유저를 찾을 수 없습니다..'}, status=status.HTTP_401_UNAUTHORIZED)

        elif request.data['email']:
            email = request.data['email']
            user = User.objects.filter(email=email)
            if user is None:
                return Response(data={'error': '유저를 찾을 수 없습니다..'}, status=status.HTTP_401_UNAUTHORIZED)
        elif request.data['phone_number']:
            phone_number = request.data['username']

        else:
            return Response(data={'error': '아이디 혹은 이메일 혹은 핸드폰 번호를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)


        # username = serializer.validated_data['username']
        # email = serializer.validated_data['email']
        # phone_number = serializer.validated_data['phone_number']

        serializer = LoginSerializer(data=request.data)
        breakpoint
        if serializer.is_valid():
            breakpoint()
            serializer.save()
            return Response(serializer.data, status=200)

        # username = request.data['username']
        # password = request.data['password']
        #
        # if (username is None) or (password is None):
        #     return Response(data={'message': 'username 이나 password를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        # user = User.objects.filter(username=username)
# class LoginView(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return Response(data={'success': '로그인 완료'}, status=status.HTTP_200_OK)
#             else:
#                 return Response(data={'error': '아이디 또는 비밀번호가 틀립니다.'}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response(data={'error': '아이디가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


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

# class ChangePasswordView(APIView):
#     def get_object(self, pk):
#         try:
#             qs = User.objects.get(pk=pk)
#             return qs
#         except ObjectDoesNotExist:
#             return None
#
#     def put(self, request, pk):
#         user = self.get_object(pk)
#         auth_number = int(request.data['auth_number'])
#         if user.auth_number == auth_number:
#             ChangePasswordSerializer(user, data=request.data, many=True)
#             return Response(data={'success': '비밀번호 변경 완료'}, status=status.HTTP_200_OK)
#         else:
#             return Response(data={'error': '인증번호가 틀립니다.'}, status=status.HTTP_401_UNAUTHORIZED)


# class RegistrationAPI(generics.GenericAPIView):
#     serializer_class = CreateUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         # if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
#         #     body = {"message": "short field"}
#         #     return Response(body, status=status.HTTP_400_BAD_REQUEST)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data={'success'})
#
#
# class LoginAPI(generics.GenericAPIView):
#     serializer_class = LoginUserSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # user = serializer.validated_data
#         return Response(data={'success' : '로그인 되었습니다.'})
