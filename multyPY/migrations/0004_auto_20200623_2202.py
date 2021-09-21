# Generated by Django 3.0.6 on 2020-06-23 22:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multyPY', '0003_auto_20200623_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='exam',
            name='number_of_correct',
            field=models.IntegerField(default=0),
        ),
    ]