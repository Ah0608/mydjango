from django.db import models


class DisPlatform(models.Model):
    task_name = models.CharField(max_length=50,verbose_name='任务名称',unique=True)
    python_path = models.CharField(max_length=500,verbose_name='解释器路径',default='python')
    task_file = models.CharField(max_length=500, verbose_name='任务文件')
    env_variable = models.CharField(max_length=500, verbose_name='环境变量',default='')
    job_id = models.CharField(max_length=100, verbose_name='任务ID',unique=True)
    time_type = models.CharField(max_length=100, verbose_name='定时类型')
    trigger_args = models.CharField(max_length=500,verbose_name='定时参数')
    scheduler_state = models.BooleanField(default=False,verbose_name='调度状态')


