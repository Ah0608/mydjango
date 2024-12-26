# Generated by Django 4.2.11 on 2024-05-10 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_apscheduler', '0009_djangojobexecution_unique_job_executions'),
        ('dispatchplatform', '0002_remove_displatform_task_args'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displatform',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_apscheduler.djangojob', verbose_name='任务ID'),
        ),
    ]
