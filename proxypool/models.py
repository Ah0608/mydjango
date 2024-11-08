from django.db import models

# Create your models here.


class ProxyPool(models.Model):
    ip = models.CharField(max_length=50,unique=True,verbose_name='代理IP')
    type = models.CharField(max_length=20,verbose_name='IP类型')
    speed = models.CharField(max_length=10,verbose_name='平均速度')
    validation_time = models.DateTimeField(auto_now_add=True,verbose_name='验证时间')