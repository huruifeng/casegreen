# Generated by Django 3.2.5 on 2022-10-04 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycase', '0004_auto_20221004_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visabulletin',
            name='adddate',
            field=models.DateField(default=datetime.datetime(2022, 10, 4, 22, 58, 2, 90444)),
        ),
        migrations.AlterField(
            model_name='visabulletin',
            name='formonth',
            field=models.CharField(default='', max_length=32),
        ),
    ]