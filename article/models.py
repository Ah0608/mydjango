from django.db import models
from mdeditor.fields import MDTextField

from user.models import User


class Article(models.Model):

    title = models.CharField(max_length=100, verbose_name='文章标题')
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='文章作者')
    intro = models.TextField(verbose_name='文章简介')
    category = models.CharField(max_length=100,verbose_name='文章分类')
    content = MDTextField(verbose_name='文章内容')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    is_delete = models.BooleanField(default=False,verbose_name='是否删除')

    def __str__(self):
        return self.title