# Generated by Django 3.2.5 on 2022-09-10 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycase', '0004_auto_20220908_2207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status_daily',
            old_name='rfe_n',
            new_name='hold_n',
        ),
        migrations.AddField(
            model_name='status_daily',
            name='mailed_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='notice_sent_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='pending_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='produced_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='return_hold_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='rfe_received_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='rfe_sent_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='status_daily',
            name='withdrawal_acknowledged_n',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]