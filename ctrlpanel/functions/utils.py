import csv
import json
import shutil

import pandas as pd

from datetime import datetime, timezone, timedelta, date
from django.core.exceptions import PermissionDenied

from mycase.models import *

timezone_offset = -4.0  # Boston Time (UTC−04:00)
tzinfo = timezone(timedelta(hours=timezone_offset))

center_dict = {"lin_lb":case_status_lin_lb,
               "msc_lb":case_status_msc_lb,
               "src_lb":case_status_src_lb,
               "wac_lb":case_status_wac_lb,
               "eac_lb":case_status_eac_lb,
               "ysc_lb":case_status_ysc_lb,
               "lin_sc":case_status_lin_sc,
               "msc_sc":case_status_msc_sc,
               "src_sc":case_status_src_sc,
               "wac_sc":case_status_wac_sc,
               "eac_sc":case_status_eac_sc,
               "ysc_sc":case_status_ysc_sc,
               "ioe":case_status_ioe
               }

def bkpTable(request,queryset):
    if not request.user.is_superuser:
        raise PermissionDenied

    model = queryset.model
    table_name = model._meta.db_table
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]

    # now = datetime.now()
    # year = str(now.year)
    # month = str(now.month)
    # day = str(now.day)
    # file_name =  "mycase/data/bkp/db_tables/export_"+table_name+"_"+month+day+year+".csv"
    file_name =  "mycase/data/bkp/db_tables/export_"+table_name+".csv"
    fp = open(file_name,"w", newline='',encoding='utf-8')
    # the csv writer
    writer = csv.writer(fp, delimiter=",")
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        writer.writerow(values)
    fp.close()

    return "OK"

def run_initalization(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    ## status
    case_status_df = pd.read_csv("mycase/data/case_status.csv",header=0,index_col=None,sep=",")
    for row_i in case_status_df.index:
        status_info = case_status_df.loc[row_i,:].to_numpy()
        status_x, created = status.objects.update_or_create(name=status_info[0],
                                                            defaults={
                                                                "name":status_info[0],
                                                                "l1": status_info[1],
                                                                "l2": status_info[2],
                                                                "l3": status_info[3],
                                                                "l4": status_info[4],
                                                                "add_date":datetime.now()
                                                            })
    ## forms
    uscis_forms_df = pd.read_csv("mycase/data/case_forms.csv",header=0,index_col=None,sep=",")
    for row_i in uscis_forms_df.index:
        form_info = uscis_forms_df.loc[row_i,:].to_numpy()
        form_x, created = form.objects.update_or_create(code=form_info[0],
                                                            defaults={
                                                                "code":form_info[0],
                                                                "name": form_info[1],
                                                                "description": form_info[2],
                                                                "add_date":datetime.now()
                                                            })

    return "OK"


def run_center(request,center):
    if not request.user.is_superuser:
        raise PermissionDenied

    sys_params = sysparam.objects.get(pk=1)
    year_n = sys_params.fiscal_year_n
    crawler_n = sys_params.crawler_number

    fiscal_years = []
    now = datetime.now()
    now_days =  (datetime.date(now) - date(2000, 1, 1)).days
    now_year = now.year - 2000
    now_month = now.month

    for i in range(year_n):
        fiscal_years.append(now_year-i)
    if now_month > 9:
        fiscal_years.append(now_year + 1)

    ## run crawler and read data from saved files
    if center.strip() != "":
        center_obj = center_dict[center]
    else:
        return "Error"


    c_i = center.split("_")[0].upper()
    lsi = center.split("_")[1]

    ## set center status to running
    c_running,_ = center_running.objects.update_or_create(center_lsi=c_i+"_"+lsi.upper(),defaults={
        "center_lsi":c_i + "_" + lsi.upper(),
        "status":"Running",
        "start":now,
        "end":datetime(2000,1,1,0,0,0),
        "update_day":now_days
    })

    print(fiscal_years)
    for fy_i in fiscal_years:
        if crawler_n > 0:
            ## run crawler and save data to folder
            ## subprocess.run("main.exe center_i fy_i lsi")
            pass

        ######################
        print(f"Reading data - Yesterday...")
        data_yesterday = {}
        try:
            file_i = "mycase/data/status_data/yesterday/" + c_i + "_" + str(fy_i) + "_" + lsi + "_bkp.json"
            with open(file_i) as json_file:
                data_yesterday = json.load(json_file)
        except Exception as e:
            print(e)
        print(f"Reading data - Yesterday...Done!")

        #####################
        print(f"Reading data - Today...")
        file_i = "mycase/data/status_data/current/" + c_i + "_" + str(fy_i) + "_" + lsi + ".json"
        with open(file_i) as json_file:
            data = json.load(json_file)
        shutil.move(file_i, "mycase/data/bkp/status_files/" + c_i + "_" + str(fy_i) + "_" + lsi + ".json")

        file_i = "mycase/data/status_data/current/" + c_i + "_" + str(fy_i) + "_" + lsi + "_case_final.json"
        with open(file_i) as json_file:
            data ={**data, **(json.load(json_file))}
        shutil.move(file_i, "mycase/data/bkp/status_files/" + c_i + "_" + str(fy_i) + "_" + lsi + "_case_final.json")
        print(f"Reading data - Today...Done!")

        total_x = len(data)
        n_i = 0

        case_list = []
        for case_i in data:
            n_i += 1
            if n_i % 100000 == 0:
                print(f"{c_i}-{lsi}-{fy_i}:{n_i}/{total_x}")

            # data : {case_num:[form,action_date,statue],...}
            if case_i in data_yesterday:
                ## if no status changes, nest
                if data[case_i][2] == data_yesterday[case_i][2]: continue

                ## when form == ""
                if data[case_i][0] == "":
                    if data_yesterday[case_i][0]!="":
                        data[case_i][0] = data_yesterday[case_i][0]

            try:
                time_s =data[case_i][1]
                time_x = datetime.strptime(time_s, "%B %d, %Y")
            except Exception as e:
                time_x = date.today()

            case_new = center_obj(receipt_number=case_i,form=data[case_i][0],status=data[case_i][2],
                                  action_date=data[case_i][1],
                                  action_date_x=time_x,
                                  add_date=datetime.now(),
                                  date_number=now_days)
            case_list.append(case_new)
        print(f"{center}-{fy_i}:Bulk Creating...")
        center_obj.objects.bulk_create(case_list,batch_size=3000)
        print(f"{center}-{fy_i}:Bulk Creating...Done!")

        print(f"Saving data...")
        file_i = "mycase/data/status_data/yesterday/" + c_i + "_" + str(fy_i) + "_" + lsi + "_bkp.json"
        with open(file_i,"w") as json_file:
            json.dump(data,json_file)
        print(f"Saving data...Done!")

    c_running.end = datetime.now()
    c_running.status="Updated"
    c_running.save()
    print(f"{center}-{fy_i}:Done!")

    return "OK"





