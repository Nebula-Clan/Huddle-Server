# Generated by Django 3.1.2 on 2020-10-28 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20201029_0211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='contnet_type',
            new_name='content_type',
        ),
    ]