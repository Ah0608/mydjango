# Generated by Django 4.2.11 on 2024-03-29 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
    ]
