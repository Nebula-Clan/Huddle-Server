# Generated by Django 3.1.2 on 2021-02-04 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftpost',
            name='reports_number',
            field=models.IntegerField(default=0),
        ),
    ]
