from random import randint
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    full_name = models.CharField(max_length=100, verbose_name="이름")
    phone_number = models.CharField(max_length=13, verbose_name="휴대폰 번호")
    auth_number = models.IntegerField(verbose_name="인증 번호")



