# Generated by Django 3.2.5 on 2022-10-11 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycase', '0009_auto_20221007_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status_trans',
            name='action_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='status_trans',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
