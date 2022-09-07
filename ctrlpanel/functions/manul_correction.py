from mycase.models import *
import datetime

case_status_tables = [case_status_lin_lb, case_status_msc_lb, case_status_src_lb, case_status_wac_lb,
                      case_status_eac_lb, case_status_ysc_lb,
                      case_status_lin_sc, case_status_msc_sc, case_status_src_sc, case_status_wac_sc,
                      case_status_eac_sc, case_status_ysc_sc,
                      case_status_ioe]
for table_i in case_status_tables:
    print(table_i._meta.label)
    objs = table_i.objects.all()
    i = 0
    obj_ls = []
    for obj in objs:
        i+=1
        if i % 10000 == 0:
            print("====================================")
            print(i)
        try:
            time_s = obj.action_date
            time_x = datetime.datetime.strptime(time_s,"%B %d, %Y")
            obj.action_date_x = time_x
        except Exception as e:
            print(obj.receipt_number, obj.action_date, obj.form, obj.status)
            time_x = datetime.date.today()
            obj.action_date_x = time_x

        obj_ls.append(obj)
    print("Updating...")
    table_i.objects.bulk_update(obj_ls, ['action_date_x'])
    print("Updating...Done!")
