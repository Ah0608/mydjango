# Generated by Django 4.2.11 on 2024-04-30 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_alter_article_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]
