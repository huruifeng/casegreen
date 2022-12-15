import json

import pandas as pd

from ctrlpanel.functions.utils import get_status_dict
from mycase.models import *
import datetime

# Create your views here.
center_dict = {"lin_lb": case_status_lin_lb,
               "msc_lb": case_status_msc_lb,
               "src_lb": case_status_src_lb,
               "wac_lb": case_status_wac_lb,
               "eac_lb": case_status_eac_lb,
               "ysc_lb": case_status_ysc_lb,
               "lin_sc": case_status_lin_sc,
               "msc_sc": case_status_msc_sc,
               "src_sc": case_status_src_sc,
               "wac_sc": case_status_wac_sc,
               "eac_sc": case_status_eac_sc,
               "ysc_sc": case_status_ysc_sc,
               }


# for center in center_dict:
#     print("---------------------------------")
#     print(center)
#     center_obj = center_dict[center.lower()]
#     case_qs = center_obj.objects.all().order_by("add_date")
#     case_rddate = {}
#     for case_i in case_qs:
#         if case_i.rd_date == date(2000, 1, 1): continue
#         case_rddate[case_i.receipt_number] = case_i.rd_date
#
#     print(len(case_rddate))
#     print(f"UPdating DB...")
#     i = 0
#     for case_rn in case_rddate:
#         i+=1
#         if i % 10000==0:print(i)
#         center_obj.objects.filter(receipt_number=case_rn,rd_date=date(2000, 1, 1)).update(rd_date=case_rddate[case_rn])
#
#     for fy_i in [20,21,22,23]:
#         print(f"updating JSON...{fy_i}")
#         file_i = "../../mycase/data/status_data/yesterday/" + center.upper() + "_" + str(fy_i) + "_bkp.json"
#         with open(file_i) as json_file:
#             data_yesterday = json.load(json_file)
#
#         for case_rn in data_yesterday:
#             if case_rn in case_rddate:
#                 data_yesterday[case_rn].append(case_rddate[case_rn].strftime("%m-%d-%Y"))
#             else:
#                 data_yesterday[case_rn].append("")
#
#         print(f"Saving data...")
#         with open(file_i, "w") as json_file:
#             json.dump(data_yesterday, json_file)
#         print(f"Saving data...Done!")
#
for center in center_dict:
    print("---------------------------------")
    print(center)

    for fy_i in [20,21,22,23]:
        print(f"updating JSON...{fy_i}")
        file_i = "../../mycase/data/status_data/yesterday/" + center.upper() + "_" + str(fy_i) + "_bkp.json"
        with open(file_i) as json_file:
            data_yesterday = json.load(json_file)

        for case_rn in data_yesterday:
            if data_yesterday[case_rn][3]=="":
                data_yesterday[case_rn][3] = "01-01-2000"

        print(f"Saving data...")
        with open(file_i, "w") as json_file:
            json.dump(data_yesterday, json_file)
        print(f"Saving data...Done!")

