# Generated by Django 4.2 on 2023-08-03 16:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='look',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
