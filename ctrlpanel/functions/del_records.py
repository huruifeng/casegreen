import json
import os

import pandas as pd
from ctrlpanel.functions.utils import get_status_dict
from mycase.models import *
import datetime

center_tables = [case_status_lin_lb,case_status_msc_lb,case_status_src_lb, case_status_wac_lb,case_status_eac_lb, case_status_ysc_lb,
                 case_status_lin_sc,case_status_msc_sc, case_status_src_sc,case_status_wac_sc,case_status_eac_sc, case_status_ysc_sc]

today = datetime.datetime.now()

# ##############
# for table_i in center_tables:
#     table_i.objects.filter(add_date__gte= datetime.datetime(today.year,today.month,today.day, hour=2, minute=0, second=0)).delete()
#
# folder = "../../mycase/data/statistics/overview"
# for file_i in os.listdir(folder):
#     os.remove(folder + "/" + file_i)

status_daily.objects.filter(add_date__gte= datetime.datetime(today.year,today.month,today.day, hour=2, minute=0, second=0)).delete()
# status_trans.objects.filter(add_date__gte= datetime.datetime(today.year,today.month,today.day, hour=2, minute=0, second=0)).delete()

