# Generated by Django 3.1.2 on 2020-12-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201212_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastseen',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]