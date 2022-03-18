from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from random import randint


class Auth(models.Model):
    phone_number = models.CharField(max_length=13, verbose_name="휴대폰 번호")
    auth_number = models.IntegerField(verbose_name="인증 번호")

    class Meta:
        db_table = 'auth'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000, 10000)
        super().save(*args, **kwargs)

class User(AbstractUser):
    nickname = models.CharField(max_length=100, verbose_name="별명")
    full_name = models.CharField(max_length=100, verbose_name="이름", null=True)
    phone_number = models.CharField(max_length=13, verbose_name="휴대폰 번호", null=True)
    auth_number = models.IntegerField(verbose_name="인증 번호", null=True)




# class UserManager(BaseUserManager):
#     # 일반 user 생성
#     def create_user(self, email, nickname, name, password=None):
#         breakpoint()
#         if not email:
#             raise ValueError('must have user email')
#         if not nickname:
#             raise ValueError('must have user nickname')
#         if not name:
#             raise ValueError('must have user name')
#         user = self.model(
#             email=self.normalize_email(email),
#             nickname=nickname,
#             name=name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     # 관리자 user 생성
#     def create_superuser(self, email, nickname, name, password=None):
#         user = self.create_user(
#             email,
#             password=password,
#             nickname=nickname,
#             name=name
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
#     nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
#     name = models.CharField(default='', max_length=100, null=False, blank=False)
#
#     # User 모델의 필수 field
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     # 헬퍼 클래스 사용
#     objects = UserManager()
#
#     # 사용자의 username field는 nickname으로 설정
#     USERNAME_FIELD = 'email'
#
#     # 필수로 작성해야하는 field
#     # REQUIRED_FIELDS = ['email', 'name']
#
#     def __str__(self):
#         return self.nickname



