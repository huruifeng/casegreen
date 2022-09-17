# Generated by Django 3.2.5 on 2022-09-16 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycase', '0008_auto_20220911_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='case_status_eac_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_eac_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_ioe',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_lin_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_lin_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_msc_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_msc_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_src_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_src_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_wac_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_wac_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_ysc_lb',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
        migrations.AddField(
            model_name='case_status_ysc_sc',
            name='rd_date',
            field=models.DateField(default=datetime.date(2000, 1, 1), verbose_name='date received'),
        ),
    ]