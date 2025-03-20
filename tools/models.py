from django.db import models

# Create your models here.


class ProjectCase(models.Model):
    name = models.CharField(max_length=200, verbose_name='项目名称')
    describe = models.CharField(max_length=1000, verbose_name='项目描述')
    language = models.CharField(max_length=100, verbose_name='编写语言')
    starts = models.CharField(max_length=50, verbose_name='starts')
    forks = models.CharField(max_length=50, verbose_name='forks')
    date_range = models.CharField(max_length=50, verbose_name='日期范围')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
