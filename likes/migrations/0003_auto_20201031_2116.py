# Generated by Django 3.1.2 on 2020-10-31 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_auto_20201031_2108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user_id',
            new_name='user',
        ),
    ]