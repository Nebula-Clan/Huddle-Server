# Generated by Django 3.1.2 on 2020-11-01 20:06

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20201029_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banner_picture',
            field=models.ImageField(null=True, upload_to=authentication.models.get_user_directory),
        ),
    ]