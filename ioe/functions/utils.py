import json
import shutil

from datetime import date, datetime, timezone, timedelta

from ctrlpanel.functions.utils import get_rd_status, get_status_dict
from mycase.functions.utils import overview_x
from mycase.models import *

timezone_offset = -4.0  # Boston Time (UTC−04:00)
tzinfo = timezone(timedelta(hours=timezone_offset))


# rd_status = ["Fees Were Waived", "Card Was Received By USCIS Along With My Letter", "Case Accepted By The USCIS Lockbox",
#              "Case Was Received", "Case Was Received and A Receipt Notice Was Sent", "Case Was Received At Another USCIS Office",
#              "Document and Letter Was Received", "Document And Letter Was Received And Under Review",
#              "Fingerprint Fee Was Received","Immigrant Visa Fee Payment Received"]

rd_status = get_rd_status()

def run_center_ioe(request,center):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return "Login: Please Login!"

    sys_params = sysparam.objects.get(pk=1)
    crawler_n = sys_params.crawler_number

    now = datetime.now()
    now_days = (now - datetime(2000, 1, 1)).days
    now_year = now.year - 2000

    ## run crawler and read data from saved files
    center = center.upper()
    print("===================================")
    print("Run:", datetime.now())

    status_dict = get_status_dict()
    counts_today = {}
    status_trans_dict = {}
    for fy_i in range(10):
        # set center status to running
        c_running, _ = center_running.objects.update_or_create(center_lsi=center + str(fy_i), defaults={
            "center_lsi": center + str(fy_i),
            "status": "Running",
            "start": now,
            "end": datetime(2000, 1, 1, 0, 0, 0),
            "update_day": now_days
        })

        print("---------------------------------")
        if crawler_n > 0:
            ## run crawler and save data to folder
            ## subprocess.run("main.exe center_i fy_i lsi")
            pass

        ######################
        print(f"Reading data - Yesterday...")
        data_yesterday = {}
        try:
            file_i = "mycase/data/status_data/yesterday/" + center + str(fy_i) + "_bkp.json"
            with open(file_i) as json_file:
                data_yesterday = json.load(json_file)
            shutil.move(file_i, "mycase/data/bkp/yesterday/" + center + str(fy_i) + "_bkp.json")
        except Exception as e:
            print(e)
        print(f"Reading data - Yesterday...Done!")

        #####################
        data_today = {}
        try:
            print(f"Reading data - Today...")
            file_i = "mycase/data/status_data/current/" + center + str(fy_i) + ".json"
            with open(file_i) as json_file:
                data_today = json.load(json_file)
            shutil.move(file_i, "mycase/data/bkp/status_files/" + center + str(fy_i) + ".json")

            file_i = "mycase/data/status_data/current/" + center + str(fy_i) + "_case_final.json"
            with open(file_i) as json_file:
                data_today ={**data_today, **(json.load(json_file))}
            shutil.move(file_i, "mycase/data/bkp/status_files/" + center + str(fy_i) + "_case_final.json")
            print(f"Reading data - Today...Done!")
        except Exception as e:
            print(e)
            c_running.end = datetime.now()
            c_running.status = "Skipped"
            c_running.save()
            print("Warning: reading "+file_i +"[Skip]")
            # return "Error: reading "+file_i

        total_x = len(data_today)
        n_i = 0

        case_list = []
        for case_i in data_today:
            form_i = data_today[case_i][0]
            act_date_i = data_today[case_i][1]
            status_i = data_today[case_i][2]

            if status_i == "try_failed": continue

            try:
                act_time_s =act_date_i
                act_time_x = datetime.strptime(act_time_s, "%B %d, %Y")
            except Exception as e:
                act_time_x = date.today()

            rd_date = date(2000, 1, 1)
            if status_i in rd_status:
                rd_date = act_time_x

            n_i += 1
            if n_i % 100000 == 0:
                print(f"{center}-{fy_i}:{n_i}/{total_x}")

            # data_today : {case_num:[form,action_date,statue],...}
            if case_i in data_yesterday:
                if data_yesterday[case_i][3] != "01-01-2000":
                    rd_date = datetime.strptime(data_yesterday[case_i][3],"%m-%d-%Y")
                ## when form == "", check saved data
                if form_i == "":
                    if data_yesterday[case_i][0] != "":
                        data_today[case_i][0] = data_yesterday[case_i][0]
                        form_i = data_yesterday[case_i][0]

                yesterday_status =  data_yesterday[case_i][2]
                if form_i != "":
                    if form_i not in status_trans_dict:
                        status_trans_dict[form_i] = {"no_yesterday":{} }
                    if yesterday_status not in status_trans_dict[form_i]:
                        status_trans_dict[form_i][yesterday_status]={}
                    if status_i in status_trans_dict[form_i][yesterday_status]:
                        status_trans_dict[form_i][yesterday_status][status_i] += 1
                    else:
                        status_trans_dict[form_i][yesterday_status][status_i] = 1

                ## if no status changes, next
                if (status_i == yesterday_status) and (act_date_i == data_yesterday[case_i][1]):
                    continue
            else:
                ## if case not in yesterday data
                if form_i != "":
                    if form_i not in status_trans_dict:
                        status_trans_dict[form_i] = {"no_yesterday": {}}

                    if status_i in status_trans_dict[form_i]["no_yesterday"]:
                        status_trans_dict[form_i]["no_yesterday"][status_i] += 1
                    else:
                        status_trans_dict[form_i]["no_yesterday"][status_i] = 1

            data_yesterday[case_i] = data_today[case_i]
            data_yesterday[case_i].append(rd_date.strftime("%m-%d-%Y"))

            ## form
            if form_i != "":
                if form_i not in counts_today:
                    counts_today[form_i]={"new_n":0,"received_n":0,"rfe_sent_n":0,"rfe_received_n":0,"approved_n":0,
                                                  "fp_schduled_n":0,"fp_taken_n":0,"iv_schduled_n":0,"iv_done_n":0,
                                                  "rejected_n":0,"terminated_n":0,"transferred_n":0,"hold_n":0,
                                                  "notice_sent_n":0,"pending_n":0,"mailed_n":0,"produced_n":0,
                                                  "return_hold_n":0,"withdrawal_acknowledged_n":0,"others_n":0}
                if status_i in rd_status:
                    counts_today[form_i]["new_n"] += 1

                if status_i in status_dict:
                    l2_name = status_dict[status_i]["L2"]
                    if l2_name == "Received": counts_today[form_i]["received_n"] += 1
                    elif l2_name == "RFE_Sent": counts_today[form_i]["rfe_sent_n"] += 1
                    elif l2_name == "RFE_Received": counts_today[form_i]["rfe_received_n"] += 1
                    elif l2_name == "Approved": counts_today[form_i]["approved_n"] += 1
                    elif l2_name == "FP_Scheduled": counts_today[form_i]["fp_schduled_n"] += 1
                    elif l2_name == "FP_Taken": counts_today[form_i]["fp_taken_n"] += 1
                    elif l2_name == "InterviewScheduled": counts_today[form_i]["iv_schduled_n"] += 1
                    elif l2_name == "InterviewCompleted": counts_today[form_i]["iv_done_n"] += 1
                    elif l2_name == "Rejected": counts_today[form_i]["rejected_n"] += 1
                    elif l2_name == "Terminated": counts_today[form_i]["terminated_n"] += 1
                    elif l2_name == "Transferred": counts_today[form_i]["transferred_n"] += 1
                    elif l2_name == "Hold": counts_today[form_i]["hold_n"] += 1
                    elif l2_name == "NoticeSent": counts_today[form_i]["notice_sent_n"] += 1
                    elif l2_name == "Pending": counts_today[form_i]["pending_n"] += 1
                    elif l2_name == "Mailed": counts_today[form_i]["mailed_n"] += 1
                    elif l2_name == "Produced": counts_today[form_i]["produced_n"] += 1
                    elif l2_name == "ReturnHold": counts_today[form_i]["return_hold_n"] += 1
                    elif l2_name == "WithdrawalAcknowledged": counts_today[form_i]["withdrawal_acknowledged_n"] += 1
                    elif l2_name == "Other": counts_today[form_i]["others_n"] += 1
                else:
                    counts_today[form_i]["others_n"] += 1

            #################
            case_stage = "Processing"
            if status_i in status_dict:
                l3_name = status_dict[status_i]["L3"]
                if l3_name in ["Approved"]:
                    case_stage = "Approved"
                elif l3_name in ["Rejected"]:
                    case_stage = "Rejected"
                elif l3_name in ["RFE"]:
                    case_stage = "RFE"
                else:
                    case_stage = "Processing"

            fy_x = rd_date.year
            if rd_date.month > 9: fy_x += 1

            case_new = case_status_ioe(receipt_number=case_i,form=form_i,status=status_i,
                                  action_date=act_date_i, action_date_x=act_time_x,
                                  case_stage = case_stage,rd_date = rd_date,
                                  add_date=datetime.now(),
                                  date_number=now_days,fiscal_year=fy_x)
            case_list.append(case_new)

        print(f"{center}-{fy_i}:Bulk Creating...")
        try:
            case_status_ioe.objects.bulk_create(case_list,batch_size=3000,ignore_conflicts=True)
        except Exception as e:
           print(e)
        print(f"{center}-{fy_i}:Bulk Creating...Done!")

        print(f"Saving data...")
        file_i = "mycase/data/status_data/yesterday/" + center + str(fy_i) + "_bkp.json"
        with open(file_i,"w") as json_file:
            json.dump(data_yesterday,json_file)
        print(f"Saving data...Done!")

        c_running.end = datetime.now()
        c_running.status="Updated"
        c_running.save()

    print("---------------------------------")
    print("Updating daily counts...")
    # update_todaycounts(now_days,center)
    print(counts_today)
    for form_ii in counts_today:
        countstoday_new = status_daily(center=center.upper(), form=form_ii,
                                       new_n=counts_today[form_ii]["new_n"],
                                       received_n=counts_today[form_ii]["received_n"],
                                       rfe_sent_n=counts_today[form_ii]["rfe_sent_n"],
                                       rfe_received_n=counts_today[form_ii]["rfe_received_n"],
                                       approved_n=counts_today[form_ii]["approved_n"],
                                       fp_schduled_n=counts_today[form_ii]["fp_schduled_n"],
                                       fp_taken_n=counts_today[form_ii]["fp_taken_n"],
                                       iv_schduled_n=counts_today[form_ii]["iv_schduled_n"],
                                       iv_done_n=counts_today[form_ii]["iv_done_n"],
                                       rejected_n=counts_today[form_ii]["rejected_n"],
                                       terminated_n=counts_today[form_ii]["terminated_n"],
                                       transferred_n=counts_today[form_ii]["transferred_n"],
                                       hold_n=counts_today[form_ii]["hold_n"],
                                       notice_sent_n=counts_today[form_ii]["notice_sent_n"],
                                       pending_n=counts_today[form_ii]["pending_n"],
                                       mailed_n=counts_today[form_ii]["mailed_n"],
                                       produced_n=counts_today[form_ii]["produced_n"],
                                       return_hold_n=counts_today[form_ii]["return_hold_n"],
                                       withdrawal_acknowledged_n=counts_today[form_ii]["withdrawal_acknowledged_n"],
                                       others_n=counts_today[form_ii]["others_n"],
                                       add_date=datetime.now(),
                                       date_number=now_days
                                       )
        countstoday_new.save(force_insert=True)
    print("Updating daily counts...Done!")

    print("---------------------------------")
    print("Updating status trans counts...")
    status_trans_ls = []
    print(status_trans_dict)
    for form_ii in status_trans_dict:
        for source_status in status_trans_dict[form_ii]:
            for dest_status in status_trans_dict[form_ii][source_status]:
                if dest_status==source_status: continue
                status_trans_new = status_trans(
                    center=center,form_type = form_ii,
                    source_status = source_status,dest_status = dest_status,
                    count = status_trans_dict[form_ii][source_status][dest_status],
                    action_date = (datetime.now().date()+timedelta(days=-1)),add_date = datetime.now(),
                    date_number = now_days,
                    fiscal_year="0", note = "" )
                status_trans_ls.append(status_trans_new)
    try:
        status_trans.objects.bulk_create(status_trans_ls, batch_size=1000,ignore_conflicts=True)
    except Exception as e:
        print(e)
    print("Updating status trans counts...Done!")

    print(f"{center}: Done!")
    return "OK"

def generate_overview_ioe():
    ####
    sys_params = sysparam.objects.get(pk=1)
    year_n = sys_params.fiscal_year_n

    year_ls = []
    now = datetime.now()
    for i in range(year_n):
        year_ls.append(str(now.year - i))
    if now.month > 9:
        if not (now.month == 10 and now.day == 1):
            ## today is 10-1, skip
            year_ls = [str(now.year + 1)] + year_ls

    for fy in year_ls:
        ok = overview_x("IOE", fy)
        if "Error" in ok:
            return "Error:Overview"
    return "OK"
