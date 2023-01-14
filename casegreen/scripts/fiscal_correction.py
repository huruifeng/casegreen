import pandas as pd

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


for center in center_dict:
    print("---------------------------------")
    print(center)
    center_obj = center_dict[center]
    case_qs = center_obj.objects.all()

    for case_i in case_qs:
        form_i = case_i.form
        status_i = case_i.status

        rn = case_i.receipt_number
        fiscal_year = int(rn[3:5])+2000
        case_i.fiscal_year = fiscal_year
        case_i.save()