from mycase.models import *
import datetime
from django.db.models import F

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
               "ioe": case_status_ioe
               }

status_ls = ["Document Was Mailed To Me",
             "Document Was Mailed",
             "Document Was Mailed But Not Returned To USCIS",
             "Document Was Mailed To Me",
             "Document Was Personally Delivered To Me"]

for center in center_dict:
    print(center)
    center_table = center_dict[center]

    case_qs = center_table.objects.filter(action_date_x__gt=F('add_date'))
    for case_i in case_qs:
        if case_i.action_date_x > case_i.add_date.date():
            if case_i.action_date_x.year >=2023:
                case_i.action_date_x = case_i.action_date_x + datetime.timedelta(days=-180)
            else:
                case_i.action_date_x = case_i.action_date_x + datetime.timedelta(days=-30)
            case_i.action_date = case_i.action_date_x.strftime("%B %d, %Y")
            case_i.save()
