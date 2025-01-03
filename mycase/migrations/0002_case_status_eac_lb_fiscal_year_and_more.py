# Generated by Django 4.1.4 on 2023-01-12 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mycase", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="case_status_eac_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_eac_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_ioe",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_lin_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_lin_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_mct_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_mct_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_msc_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_msc_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_src_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_src_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_wac_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_wac_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_ysc_lb",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="case_status_ysc_sc",
            name="fiscal_year",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
