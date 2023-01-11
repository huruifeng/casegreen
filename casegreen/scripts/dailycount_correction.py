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


case_status_df = pd.read_csv("../../mycase/data/case_status.csv", header=0, index_col=0, sep=",")
rd_status = case_status_df.loc[case_status_df["NewReceived"]=="YES",:].index.tolist()
status_dict = case_status_df.to_dict(orient="index")

start_date = datetime.datetime(2022,9,24,1,5,10)
end_date = datetime.datetime(2022,11,7,1,5,10)

add_date = start_date
while add_date <=end_date:
    print("===========================")
    print(add_date)
    date_num = (add_date - datetime.datetime(2000, 1, 1)).days

    for center in center_dict:
        print("---------------------------------")
        print(center)
        center_obj = center_dict[center.lower()]
        case_qs = center_obj.objects.filter(date_number=date_num)

        counts_today = {}
        for case_i in case_qs:
            form_i = case_i.form
            status_i = case_i.status

            ## form
            if form_i != "":
                if form_i not in counts_today:
                    counts_today[form_i] = {"new_n": 0, "received_n": 0, "rfe_sent_n": 0, "rfe_received_n": 0, "approved_n": 0,
                                            "fp_schduled_n": 0, "fp_taken_n": 0, "iv_schduled_n": 0, "iv_done_n": 0,
                                            "rejected_n": 0, "terminated_n": 0, "transferred_n": 0, "hold_n": 0,
                                            "notice_sent_n": 0, "pending_n": 0, "mailed_n": 0, "produced_n": 0,
                                            "return_hold_n": 0, "withdrawal_acknowledged_n": 0, "others_n": 0}
                if status_i in rd_status:
                    counts_today[form_i]["new_n"] += 1

                if status_i in status_dict:
                    l2_name = status_dict[status_i]["L2"]
                    if l2_name == "Received":
                        counts_today[form_i]["received_n"] += 1
                    elif l2_name == "RFE_Sent":
                        counts_today[form_i]["rfe_sent_n"] += 1
                    elif l2_name == "RFE_Received":
                        counts_today[form_i]["rfe_received_n"] += 1
                    elif l2_name == "Approved":
                        counts_today[form_i]["approved_n"] += 1
                    elif l2_name == "FP_Scheduled":
                        counts_today[form_i]["fp_schduled_n"] += 1
                    elif l2_name == "FP_Taken":
                        counts_today[form_i]["fp_taken_n"] += 1
                    elif l2_name == "InterviewScheduled":
                        counts_today[form_i]["iv_schduled_n"] += 1
                    elif l2_name == "InterviewCompleted":
                        counts_today[form_i]["iv_done_n"] += 1
                    elif l2_name == "Rejected":
                        counts_today[form_i]["rejected_n"] += 1
                    elif l2_name == "Terminated":
                        counts_today[form_i]["terminated_n"] += 1
                    elif l2_name == "Transferred":
                        counts_today[form_i]["transferred_n"] += 1
                    elif l2_name == "Hold":
                        counts_today[form_i]["hold_n"] += 1
                    elif l2_name == "NoticeSent":
                        counts_today[form_i]["notice_sent_n"] += 1
                    elif l2_name == "Pending":
                        counts_today[form_i]["pending_n"] += 1
                    elif l2_name == "Mailed":
                        counts_today[form_i]["mailed_n"] += 1
                    elif l2_name == "Produced":
                        counts_today[form_i]["produced_n"] += 1
                    elif l2_name == "ReturnHold":
                        counts_today[form_i]["return_hold_n"] += 1
                    elif l2_name == "WithdrawalAcknowledged":
                        counts_today[form_i]["withdrawal_acknowledged_n"] += 1
                    elif l2_name == "Other":
                        counts_today[form_i]["others_n"] += 1
                else:
                    counts_today[form_i]["others_n"] += 1

        print("Updating daily counts...")
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
                                           add_date = add_date + datetime.timedelta(hours=6),
                                           date_number = date_num)
            countstoday_new.save(force_insert=True)
        print("Updating daily counts...Done!")

    add_date = add_date+datetime.timedelta(days=1)