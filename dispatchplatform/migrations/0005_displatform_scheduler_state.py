# Generated by Django 4.2.11 on 2024-05-10 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatchplatform', '0004_alter_displatform_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='displatform',
            name='scheduler_state',
            field=models.BooleanField(default=False, verbose_name='调度状态'),
        ),
    ]