# Generated by Django 4.2.11 on 2024-05-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DisPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50, verbose_name='任务名称')),
                ('python_path', models.CharField(default='python', max_length=500, verbose_name='解释器路径')),
                ('task_file', models.CharField(max_length=500, verbose_name='任务文件')),
                ('job_id', models.CharField(max_length=100, unique=True, verbose_name='任务ID')),
                ('time_type', models.CharField(max_length=100, verbose_name='定时类型')),
                ('trigger_args', models.CharField(max_length=500, verbose_name='定时参数')),
                ('task_args', models.CharField(max_length=500, verbose_name='任务参数')),
            ],
        ),
    ]
