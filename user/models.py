from django.contrib.auth.models import AbstractUser
from django.db import models

from common.basedb import BaseModel


class User(AbstractUser, BaseModel):  # 同时继承AbstractUser表和BaseModel表里的字段

    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    mobile = models.CharField(max_length=11, default='', verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/',default='avatars/default_avatar.png', verbose_name='头像')

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'


class EmailVerify(models.Model):
    objects = models.Manager()

    email_address = models.CharField(max_length=50)
    verify_code = models.CharField(max_length=10)
    expiration_time = models.IntegerField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'emailing'
        verbose_name = '邮箱验证码表'