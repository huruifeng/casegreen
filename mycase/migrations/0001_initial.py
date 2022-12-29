# Generated by Django 4.1.4 on 2022-12-28 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="case_status_eac_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_eac_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_ioe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_lin_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_lin_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_mct_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_mct_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_msc_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_msc_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_src_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_src_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_wac_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_wac_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_ysc_lb",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="case_status_ysc_sc",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receipt_number", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("status", models.CharField(max_length=128)),
                ("action_date", models.CharField(max_length=32)),
                ("action_date_x", models.DateField(default=datetime.date.today)),
                ("case_stage", models.CharField(default="", max_length=32)),
                (
                    "rd_date",
                    models.DateField(
                        default=datetime.date(2000, 1, 1), verbose_name="date received"
                    ),
                ),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="center_running",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "center_lsi",
                    models.CharField(
                        choices=[
                            ("LIN_LB", "LIN_LB"),
                            ("MSC_LB", "MSC_LB"),
                            ("SRC_LB", "SRC_LB"),
                            ("WAC_LB", "WAC_LB"),
                            ("EAC_LB", "EAC_LB"),
                            ("YSC_LB", "YSC_LB"),
                            ("LIN_SC", "LIN_SC"),
                            ("MSC_SC", "MSC_SC"),
                            ("SRC_SC", "SRC_SC"),
                            ("WAC_SC", "WAC_SC"),
                            ("EAC_SC", "EAC_SC"),
                            ("YSC_SC", "YSC_SC"),
                            ("IOE", "IOE"),
                        ],
                        default="",
                        max_length=32,
                    ),
                ),
                ("status", models.CharField(max_length=16)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("update_day", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="form",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(default="", max_length=8)),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField()),
                (
                    "add_date",
                    models.DateTimeField(auto_now=True, verbose_name="date added"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("l1", models.CharField(max_length=64)),
                ("l2", models.CharField(max_length=32)),
                ("l3", models.CharField(max_length=16)),
                ("l4", models.CharField(max_length=16)),
                ("note", models.CharField(max_length=256)),
                ("add_date", models.DateTimeField(verbose_name="date added")),
            ],
        ),
        migrations.CreateModel(
            name="status_daily",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("center", models.CharField(max_length=16)),
                ("form", models.CharField(max_length=16)),
                ("new_n", models.IntegerField(default=0)),
                ("received_n", models.IntegerField()),
                ("rfe_sent_n", models.IntegerField()),
                ("rfe_received_n", models.IntegerField()),
                ("approved_n", models.IntegerField()),
                ("fp_schduled_n", models.IntegerField()),
                ("fp_taken_n", models.IntegerField()),
                ("iv_schduled_n", models.IntegerField()),
                ("iv_done_n", models.IntegerField()),
                ("rejected_n", models.IntegerField()),
                ("terminated_n", models.IntegerField()),
                ("transferred_n", models.IntegerField()),
                ("hold_n", models.IntegerField()),
                ("notice_sent_n", models.IntegerField()),
                ("pending_n", models.IntegerField()),
                ("mailed_n", models.IntegerField()),
                ("produced_n", models.IntegerField()),
                ("return_hold_n", models.IntegerField()),
                ("withdrawal_acknowledged_n", models.IntegerField()),
                ("others_n", models.IntegerField()),
                ("add_date", models.DateTimeField(verbose_name="date added")),
                ("date_number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="status_trans",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("center", models.CharField(max_length=32)),
                ("form_type", models.CharField(max_length=32)),
                ("source_status", models.CharField(max_length=128)),
                ("dest_status", models.CharField(max_length=128)),
                ("count", models.IntegerField()),
                ("fiscal_year", models.CharField(max_length=8)),
                ("action_date", models.DateField(default=datetime.datetime.now)),
                ("add_date", models.DateTimeField(default=datetime.datetime.now)),
                ("date_number", models.IntegerField()),
                ("note", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="sysparam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("centers", models.CharField(max_length=64)),
                ("fiscal_year_n", models.IntegerField()),
                ("crawler_time", models.TimeField()),
                ("crawler_number", models.IntegerField()),
                ("sys_status", models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name="visabulletin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("EBFB", models.CharField(default="", max_length=8)),
                ("category", models.CharField(default="", max_length=64)),
                (
                    "conutry",
                    models.CharField(
                        choices=[
                            ("CHINA", "China"),
                            ("INDIA", "India"),
                            ("MEXICO", "Mexico"),
                            ("PHILIPPINES", "Philippines"),
                            ("EGH", "El Salvador/Guatemala/Honduras"),
                            ("OTHERS", "Others"),
                        ],
                        default="",
                        max_length=32,
                    ),
                ),
                ("tableA", models.CharField(max_length=8)),
                ("tableB", models.CharField(max_length=8)),
                ("formonth", models.CharField(default="", max_length=32)),
                ("visadate", models.CharField(max_length=128)),
                ("adddate", models.DateField(auto_now=True)),
                ("description", models.TextField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="case_status_ysc_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_ysc_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_ysc_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_ysc_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_wac_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_wac_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_wac_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_wac_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_src_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_src_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_src_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_src_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_msc_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_msc_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_msc_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_msc_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_mct_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_mct_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_mct_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_mct_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_lin_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_lin_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_lin_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_lin_lb",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_ioe",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_ioe",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_eac_sc",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_eac_sc",
            ),
        ),
        migrations.AddConstraint(
            model_name="case_status_eac_lb",
            constraint=models.UniqueConstraint(
                fields=("receipt_number", "status", "action_date_x"),
                name="unique_receipt_status_datex_eac_lb",
            ),
        ),
    ]
