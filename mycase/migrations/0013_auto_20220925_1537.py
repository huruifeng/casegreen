# Generated by Django 3.2.5 on 2022-09-25 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycase', '0012_auto_20220925_1532'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='case_status_eac_lb',
            name='unique_receipt_status_datex_eac_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_eac_sc',
            name='unique_receipt_status_datex_eac_sc',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_ioe',
            name='unique_receipt_status_datex_ioe',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_lin_lb',
            name='unique_receipt_status_datex_lin_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_lin_sc',
            name='unique_receipt_status_datex_lin_sc',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_msc_lb',
            name='unique_receipt_status_datex_msc_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_msc_sc',
            name='unique_receipt_status_datex_msc_sc',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_src_lb',
            name='unique_receipt_status_datex_src_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_src_sc',
            name='unique_receipt_status_datex_src_sc',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_wac_lb',
            name='unique_receipt_status_datex_wac_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_wac_sc',
            name='unique_receipt_status_datex_wac_sc',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_ysc_lb',
            name='unique_receipt_status_datex_ysc_lb',
        ),
        migrations.RemoveConstraint(
            model_name='case_status_ysc_sc',
            name='unique_receipt_status_datex_ysc_sc',
        ),
        migrations.AddConstraint(
            model_name='case_status_eac_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_eac_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_eac_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_eac_sc'),
        ),
        migrations.AddConstraint(
            model_name='case_status_ioe',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_ioe'),
        ),
        migrations.AddConstraint(
            model_name='case_status_lin_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_lin_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_lin_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_lin_sc'),
        ),
        migrations.AddConstraint(
            model_name='case_status_msc_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_msc_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_msc_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_msc_sc'),
        ),
        migrations.AddConstraint(
            model_name='case_status_src_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_src_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_src_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_src_sc'),
        ),
        migrations.AddConstraint(
            model_name='case_status_wac_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_wac_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_wac_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_wac_sc'),
        ),
        migrations.AddConstraint(
            model_name='case_status_ysc_lb',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_ysc_lb'),
        ),
        migrations.AddConstraint(
            model_name='case_status_ysc_sc',
            constraint=models.UniqueConstraint(fields=('receipt_number', 'status', 'action_date_x'), name='unique_receipt_status_date_ysc_sc'),
        ),
    ]
