# Generated by Django 4.2 on 2024-04-04 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.png', null=True, upload_to='avatars/', verbose_name='头像'),
        ),
    ]
