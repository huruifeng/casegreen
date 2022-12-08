## Function library
import json
import os.path
from datetime import date, timedelta, datetime

import numpy as np
import requests
from bs4 import BeautifulSoup
import re

from django.db.models import Count

from ctrlpanel.functions.utils import get_status_dict
from mycase.models import *

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# LIN – Lincoln Service Center (Nebraska Service Center)
# EAC – Eastern Adjudication Center (Vermont Service Center)
# IOE – USCIS Electronic Immigration System (ELIS)
# WAC – Western Adjudication Center (California Service Center)
# MSC – Missouri Service Center (National Benefits Center)
# NBC – National Benefits Center
# SRC – Southern Regional Center (Texas Service Center)
# YSC - Potomac Service Center
center_names = ["MSC", "LIN", "SRC", "WAC", "EAC", "IOE", "YSC"]

form_types = [
    "I-129CW",
    "I-129F",
    "I-600A",
    "I-601A",
    "I-765V",
    "I-485J",
    "I-800A",
    "I-821D",
    "I-90",
    "I-102",
    "I-129",
    "I-130",
    "I-131",
    "I-140",
    "I-212",
    "I-360",
    "I-485",
    "I-526",
    "I-539",
    "I-600",
    "I-601",
    "I-612",
    "I-730",
    "I-751",
    "I-765",
    "I-800",
    "I-817",
    "I-821",
    "I-824",
    "I-829",
    "I-914",
    "I-918",
    "I-924",
    "I-929"
]

color20 = {'Received': '#1266f1', 'Transferred': '#17becf', 'Pending': '#ff7f0e',
           'FP_Scheduled': '#1f77b4', 'FP_Taken': '#aec7e8', 'InterviewScheduled': '#9467bd',
           'InterviewCompleted': '#c5b0d5',
           'RFE_Sent': '#bcbd22', 'RFE_Received': '#dbdb8d', 'Approved': '#2ca02c', 'Produced': '#98df8a',
           'Mailed': '#a1d99b',
           'Hold': '#ffbb78', 'ReturnHold': '#8c564b', 'NoticeSent': '#c49c94', 'Reopened': '#e377c2',
           'Other': '#f7b6d2',
           'Rejected': '#d62728', 'Terminated': '#ff9896', 'bk1': '#7f7f7f', 'bk2': '#c7c7c7', 'bk3': '#9edae5'}

color8 = {'Received': "#1072f1", 'FP_Taken': "#11a9fa", 'Interviewed': "#2b04da", 'RFE': "#f4b824",
          'Transferred': "#c77cff", 'Approved': "#1db063", 'Rejected': "#ff001a", 'Other': "#78787a"}

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

rd_status = ["Fees Were Waived", "Card Was Received By USCIS Along With My Letter",
             "Case Accepted By The USCIS Lockbox",
             "Case Was Received", "Case Was Received and A Receipt Notice Was Sent",
             "Case Was Received At Another USCIS Office",
             "Document and Letter Was Received", "Document And Letter Was Received And Under Review",
             "Fingerprint Fee Was Received"]

status_dict = get_status_dict()


def get_status(recepit_number):
    ## Test
    # recepit_number="LIN2290104917"

    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    case_data = {"appReceiptNum": recepit_number}

    try_n = 0
    while True:
        ## Try N times at most
        try:
            resp = requests.post(url, data=case_data, verify=False)
            try_n += 1
            if resp.status_code in [200]:
                break
            else:
                if try_n >= 10:
                    return ["try_failed", resp.status_code]
        except Exception as e:
            try_n += 1
            if try_n >= 10:
                return ["try_failed", e]

    soup = BeautifulSoup(resp.text, 'html.parser')
    status_div = soup.find("div", class_="rows text-center")
    if status_div:
        ## case exists
        status_h_text = status_div.h1.get_text(strip=True)
        if status_h_text.strip() == "":
            return ["error", "invlid_num"]

        status_p_text = status_div.p.get_text()
        status_p_text_ls = re.split(" |,", status_p_text)
        status_p_text_ls = [i for i in status_p_text_ls if i]

        date = ""
        form = ""
        n_words = len(status_p_text_ls)
        for i in range(n_words):
            if status_p_text_ls[i] in months:
                if date == "":
                    date = status_p_text_ls[i] + " " + status_p_text_ls[i + 1] + ", " + status_p_text_ls[i + 2]
            elif status_p_text_ls[i] == "Form":
                form = status_p_text_ls[i + 1]
                break
        if form == "":
            for form_x in form_types:
                if form_x in status_p_text:
                    form = form_x
                    break
        if date != "":
            status_p_text = status_p_text.replace(date, "<u>" + date + "</u>")
        if form != "":
            status_p_text = status_p_text.replace(form, "<u>" + form + "</u>")

        status_p_text = status_p_text.replace(recepit_number, "<u>" + recepit_number + "</u>")
        return [form, date, status_h_text, status_p_text]
    else:
        ## the case number is invlid
        return ["error", "invlid_num"]


def get_l_status(status_str, l="L3"):
    if l == "L0" or l=="Status": return status_str
    if status_str in status_dict:
        l_name = status_dict[status_str][l.upper()]
    else:
        l_name = "Other"
    return l_name


def getcase_in_range(case_range, center, case_range_base, center_table, form_type, receipt_num):
    if case_range == "rn_range":
        case_range_s = center + str(case_range_base)
        case_range_e = center + str(case_range_base + 4999)
        case_qs = center_table.objects.filter(form=form_type, receipt_number__range=(case_range_s, case_range_e))
    elif case_range == "rn_n200":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:201]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_n500":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:501]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_n1000":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:1001]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_p200":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:201]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_p500":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:501]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_p1000":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:1001]]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
    elif case_range == "rn_np200":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values(
            "receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:200]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:201]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rn_np500":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values(
            "receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:500]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:501]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rn_np1000":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values(
            "receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:1000]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values(
            "receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:1001]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rd_n1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-30)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_n2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-60)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_n3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-90)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_p1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+30)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_p2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+60)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_p3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+90)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_np1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-30)
            case_rd_e = case_rd.rd_date + timedelta(days=+30)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_np2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-60)
            case_rd_e = case_rd.rd_date + timedelta(days=+60)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    elif case_range == "rd_np3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-90)
            case_rd_e = case_rd.rd_date + timedelta(days=+90)
            case_rd_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
            case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
            case_rn_rd = {}
            for case_rd_i in case_rd_qs:
                case_rn_rd[case_rd_i["receipt_number"]] = case_rd_i["rd_date"]
            case_rn_ls = list(case_rn_rd.keys())
            case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls)
        else:
            case_qs = []
    # elif case_range == "rn_fy":
    #     center_year = center + year
    #     case_qs = center_table.objects.filter(form=form_type, receipt_number__startswith=center_year)
    else:
        case_range_s = center + str(case_range_base)
        case_range_e = center + str(case_range_base + 4999)
        case_qs = center_table.objects.filter(form=form_type, receipt_number__range=(case_range_s, case_range_e))

    return case_qs


def get_rnrangecount(center_table, center, selectform, fy, statuslevel, rangesize):
    fy = fy[-2:]
    c_code = center.split("_")[0]
    rn_range = int(rangesize)

    if statuslevel == "L3":
        color = color8
        dataset_labels = ['Received', 'FP_Taken', 'Interviewed', 'RFE', 'Transferred', 'Approved', 'Rejected', 'Other']
    if statuslevel == "L2":
        color = color20
        dataset_labels = ['Received', 'FP_Scheduled', 'FP_Taken', 'InterviewScheduled', 'InterviewCompleted',
                          'RFE_Sent', 'RFE_Received', 'Transferred', 'Approved', 'Produced', 'Mailed', 'Pending',
                          'Hold', 'ReturnHold', 'NoticeSent', 'Reopened', 'Other', 'Rejected', 'Terminated',
                          'WithdrawalAcknowledged']

    ## Check if there is the statistics file for the selected options
    ## first time visiting will save the results to json file
    file_name = "_".join([center, selectform, fy, statuslevel, rangesize]) + ".json"
    folder = "mycase/data/statistics/center_range_count"
    file_name = folder + "/" + file_name
    if os.path.exists(file_name):
        try:
            with open(file_name) as json_file:
                data_dict = json.load(json_file)
            return data_dict
        except Exception as e:
            print(e)

    #####################
    rn_pattern = c_code + fy
    case_qs = center_table.objects.filter(form=selectform, receipt_number__startswith=rn_pattern).order_by(
        "receipt_number", "-add_date")

    status_count = {}
    rn_status = {}
    for case_i in case_qs:
        if case_i.receipt_number in rn_status: continue
        status_l = get_l_status(case_i.status, statuslevel)
        rn_status[case_i.receipt_number] = 1

        rn = int(case_i.receipt_number[3:])
        range_key = rn - (rn % rn_range)

        if range_key not in status_count:
            if statuslevel == "L2":
                status_count[range_key] = {
                    'Received': 0, 'FP_Scheduled': 0, 'FP_Taken': 0, 'InterviewScheduled': 0, 'InterviewCompleted': 0,
                    'RFE_Sent': 0, 'RFE_Received': 0, 'Transferred': 0, 'Approved': 0, 'Produced': 0, 'Mailed': 0,
                    'Pending': 0, 'Hold': 0, 'ReturnHold': 0, 'NoticeSent': 0, 'Reopened': 0, 'Other': 0, 'Rejected': 0,
                    'Terminated': 0, 'WithdrawalAcknowledged': 0
                }

            if statuslevel == "L3":
                status_count[range_key] = {
                    'Received': 0, 'FP_Taken': 0, 'Interviewed': 0, 'RFE': 0, 'Transferred': 0, 'Approved': 0,
                    'Rejected': 0, 'Other': 0
                }
        status_count[range_key][status_l] += 1

    labels = [c_code + str(i) + "-" + str(i + rn_range - 1)[-4:] for i in status_count]
    dataset = {}
    for dataset_i in dataset_labels:
        dataset[dataset_i] = []
        for rnrange_i in status_count:
            dataset[dataset_i].append(status_count[rnrange_i][dataset_i])

    data_dict = {"dataset": dataset, "label": labels, "color": color}
    with open(file_name, "w") as json_file:
        json.dump(data_dict, json_file)

    return data_dict


def get_rdcount(center_table, center, selectform, fy, statuslevel, rangesize):
    fy = int(fy)
    rd_range_min = date(fy - 1, 10, 1)
    rd_range_max = date(fy, 9, 30)
    fy = str(fy)[-2:]

    if statuslevel == "L3":
        color = color8
        dataset_labels = ['Received', 'FP_Taken', 'Interviewed', 'RFE', 'Transferred', 'Approved', 'Rejected', 'Other']
    if statuslevel == "L2":
        color = color20
        dataset_labels = ['Received', 'FP_Scheduled', 'FP_Taken', 'InterviewScheduled', 'InterviewCompleted',
                          'RFE_Sent', 'RFE_Received', 'Transferred', 'Approved', 'Produced', 'Mailed', 'Pending',
                          'Hold', 'ReturnHold', 'NoticeSent', 'Reopened', 'Other', 'Rejected', 'Terminated',
                          'WithdrawalAcknowledged']

    ## Check if there is the statistics file for the selected options
    ## first time visiting will save the results to json file
    file_name = "_".join([center, selectform, fy, statuslevel, rangesize]) + ".json"
    folder = "mycase/data/statistics/center_rd_count"
    file_name = folder + "/" + file_name
    if os.path.exists(file_name):
        try:
            with open(file_name) as json_file:
                data_dict = json.load(json_file)
            return data_dict
        except Exception as e:
            print(e)

    ####################
    ## build range keys
    if rangesize not in ["weekly", "monthly"]:
        rangesize = "weekly"
    rd_x = rd_range_min
    range_keys = {}
    if rangesize == "weekly":
        while rd_x < rd_range_max:
            rd_wkn = rd_x.isocalendar()[1]
            range_keys[rd_wkn] = rd_x.strftime("%m-%d-%Y:w%U")
            rd_x += timedelta(weeks=+1)
    else:
        while rd_x < rd_range_max:
            rd_mhn = rd_x.month
            range_keys[rd_mhn] = rd_x.strftime("%b-%Y")
            rd_x += timedelta(days=+31)

    #####################
    case_rn_rd = {}
    case_rd_qs = center_table.objects.filter(form=selectform, rd_date__range=(rd_range_min, rd_range_max)).order_by(
        "rd_date")
    case_rd_qs = case_rd_qs.values("receipt_number", "rd_date").distinct()
    for case_rd_i in case_rd_qs:
        case_rn_rd[case_rd_i["receipt_number"]] = [case_rd_i["rd_date"]]
    case_rn_ls = list(case_rn_rd.keys())

    case_qs = center_table.objects.filter(receipt_number__in=case_rn_ls).order_by("-add_date").values("receipt_number",
                                                                                                      "status")

    rn_status = {}
    for case_i in case_qs:
        if case_i["receipt_number"] in rn_status: continue
        status_l = get_l_status(case_i["status"], statuslevel)
        rn_status[case_i["receipt_number"]] = 1
        case_rn_rd[case_i["receipt_number"]].append(status_l)

    status_count = {}
    for case_rn in case_rn_rd:
        rd_i = case_rn_rd[case_rn][0]
        if rangesize == "weekly":
            rd_i_no = rd_i.isocalendar()[1]
        else:
            rd_i_no = rd_i.month
        range_key = range_keys[rd_i_no]

        if range_key not in status_count:
            if statuslevel == "L2":
                status_count[range_key] = {
                    'Received': 0, 'FP_Scheduled': 0, 'FP_Taken': 0, 'InterviewScheduled': 0, 'InterviewCompleted': 0,
                    'RFE_Sent': 0, 'RFE_Received': 0, 'Transferred': 0, 'Approved': 0, 'Produced': 0, 'Mailed': 0,
                    'Pending': 0, 'Hold': 0, 'ReturnHold': 0, 'NoticeSent': 0, 'Reopened': 0, 'Other': 0, 'Rejected': 0,
                    'Terminated': 0, 'WithdrawalAcknowledged': 0
                }
            elif statuslevel == "L3":
                status_count[range_key] = {
                    'Received': 0, 'FP_Taken': 0, 'Interviewed': 0, 'RFE': 0, 'Transferred': 0, 'Approved': 0,
                    'Rejected': 0, 'Other': 0
                }
        status_count[range_key][case_rn_rd[case_rn][1]] += 1

    dataset = {}
    for dataset_i in dataset_labels:
        dataset[dataset_i] = []
        for rdrange_i in status_count:
            dataset[dataset_i].append(status_count[rdrange_i][dataset_i])

    data_dict = {"dataset": dataset, "label": list(status_count.keys()), "color": color}
    with open(file_name, "w") as json_file:
        json.dump(data_dict, json_file)
    return data_dict


def get_dailyrecords(center="", selectform="", date_number=0):
    if date_number == 0:
        date_s = datetime.today() + timedelta(days=-365)
        if date_s < datetime(2022, 9, 26):
            date_s = datetime(2022, 9, 26)  ## 09-25-2022 is the first data date

        count_qs = status_daily.objects.filter(form=selectform, center=center, add_date__gte=date_s).order_by(
            "add_date")
        date_ls = []
        rec = []
        fp = []
        itv = []
        rfe = []
        trf = []
        apv = []
        rej = []
        oth = []
        pending = []
        for count_i in count_qs:
            date_ls.append((count_i.add_date.date() + timedelta(days=-1)).strftime("%m-%d-%Y"))
            rec.append(count_i.new_n)
            fp.append(count_i.fp_taken_n + count_i.fp_schduled_n)
            itv.append(count_i.iv_schduled_n + count_i.iv_done_n)
            rfe.append(count_i.rfe_sent_n + count_i.rfe_received_n)
            trf.append(count_i.transferred_n)
            apv.append(count_i.approved_n + count_i.mailed_n + count_i.produced_n)
            # rej.append(count_i.rejected_n + count_i.terminated_n)
            rej.append(count_i.rejected_n)
            pending.append(count_i.pending_n)
            oth.append(
                count_i.others_n + count_i.notice_sent_n + count_i.hold_n + count_i.return_hold_n + count_i.withdrawal_acknowledged_n)

        count_ls = [rec, fp, itv, rfe, trf, apv, rej, oth, pending]
        data_dict = {"label_ls": date_ls, "count_ls": count_ls}
        return data_dict
    else:
        count_dict = {}
        count_qs = status_daily.objects.filter(center=center, date_number=date_number)
        for count_i in count_qs:
            count_dict[count_i.form] = {"rec_d": count_i.new_n,
                                        "fp_d": count_i.fp_taken_n + count_i.fp_schduled_n,
                                        "itv_d": count_i.iv_schduled_n + count_i.iv_done_n,
                                        "rfe_d": count_i.rfe_sent_n + count_i.rfe_received_n,
                                        "trf_d": count_i.transferred_n,
                                        "apv_d": count_i.approved_n + count_i.mailed_n + count_i.produced_n,
                                        # "rej_d":count_i.rejected_n + count_i.terminated_n,
                                        "rej_d": count_i.rejected_n,
                                        "pending_d": count_i.pending_n,
                                        "oth_d": count_i.others_n + count_i.notice_sent_n + count_i.hold_n + count_i.return_hold_n + count_i.withdrawal_acknowledged_n}
        return count_dict


def get_ytdcount(endDate):
    if endDate.month >= 10:
        fy = endDate.year + 1
    else:
        fy = endDate.year

    start_s = datetime(int(fy) - 1, 10, 2)
    end_s = endDate + timedelta(days=2)

    count_dict = {}
    count_qs = status_daily.objects.filter(add_date__range=(start_s, end_s))
    for count_i in count_qs:
        if count_i.center not in count_dict:
            count_dict[count_i.center] = {}
            count_dict[count_i.center][count_i.form] = {"rec_y": 0, "fp_y": 0, "itv_y": 0, "rfe_y": 0, "trf_y": 0,
                                                        "apv_y": 0, "rej_y": 0, "pending_y": 0, "oth_y": 0}
        else:
            if count_i.form not in count_dict[count_i.center]:
                count_dict[count_i.center][count_i.form] = {"rec_y": 0, "fp_y": 0, "itv_y": 0, "rfe_y": 0, "trf_y": 0,
                                                            "apv_y": 0, "rej_y": 0, "pending_y": 0, "oth_y": 0}

        count_dict[count_i.center][count_i.form]["rec_y"] += count_i.new_n
        count_dict[count_i.center][count_i.form]["fp_y"] += count_i.fp_taken_n + count_i.fp_schduled_n
        count_dict[count_i.center][count_i.form]["itv_y"] += count_i.iv_schduled_n + count_i.iv_done_n
        count_dict[count_i.center][count_i.form]["rfe_y"] += count_i.rfe_sent_n + count_i.rfe_received_n
        count_dict[count_i.center][count_i.form]["trf_y"] += count_i.transferred_n
        count_dict[count_i.center][count_i.form]["apv_y"] += count_i.approved_n + count_i.mailed_n + count_i.produced_n
        count_dict[count_i.center][count_i.form]["rej_y"] += count_i.rejected_n
        count_dict[count_i.center][count_i.form]["pending_y"] += count_i.pending_n
        count_dict[count_i.center][count_i.form][
            "oth_y"] += count_i.others_n + count_i.notice_sent_n + count_i.hold_n + count_i.return_hold_n + count_i.withdrawal_acknowledged_n

    return count_dict


def generate_overview(center_ls):
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

    ## Check if there is the statistics file for the selected options
    ## first time visiting will save the results to json file
    for center_i in center_ls:
        for fy in year_ls:
            ok = overview_x(center_i, fy)
            if "Error" in ok:
                return "Error:Overview"
    return "OK"


def overview_x(center, fy):
    file_name = "_".join([center.upper(), fy[-2:]]) + ".json"
    folder = "mycase/data/statistics/overview"
    file_name = folder + "/" + file_name

    center_table = center_dict[center.lower()]
    rn_pattern = center.upper().split("_")[0] + fy[-2:]
    case_qs = center_table.objects.filter(receipt_number__startswith=rn_pattern).order_by("receipt_number", "-add_date")

    form_status_count = {}
    rn_status = {}
    for case_i in case_qs:
        if case_i.receipt_number in rn_status: continue
        status_l = get_l_status(case_i.status, "L3")
        rn_status[case_i.receipt_number] = 1
        form_type = case_i.form
        if form_type == "":
            form_type = "Unknown"
        if form_type not in form_status_count:
            form_status_count[form_type] = {}
            form_status_count[form_type][status_l] = 1
        else:
            if status_l not in form_status_count[form_type]:
                form_status_count[form_type][status_l] = 1
            else:
                form_status_count[form_type][status_l] += 1

    try:
        with open(file_name, "w") as json_file:
            json.dump(form_status_count, json_file)
    except Exception as e:
        print(e)
        return "Error:Dump"

    return "OK"

def get_rangestatuscount(center, fy, selectform, rangesize):
    ## Check if there is the statistics file for the selected options
    ## first time visiting will save the results to json file
    file_name = "_".join([center, selectform, fy, rangesize]) + ".json"
    folder = "mycase/data/statistics/center_range_count_heatmap"
    file_name = folder + "/" + file_name
    if os.path.exists(file_name):
        try:
            with open(file_name) as json_file:
                data_dict = json.load(json_file)
            return data_dict
        except Exception as e:
            print(e)

    #####################
    rn_range = int(rangesize)
    fy = fy[-2:]
    c_code = center.split("_")[0]

    center_table = center_dict[center.lower()]

    date_s = datetime.now() + timedelta(days=-60)

    rn_pattern = c_code + fy
    case_qs = center_table.objects.filter(form=selectform, receipt_number__startswith=rn_pattern,
                                          action_date_x__gte=date_s).order_by("receipt_number")
    date_ls = [(date_s + timedelta(days=i)).strftime("%m-%d-%Y") for i in range(60)]

    range_ls = []

    status_count = {'New': {}, 'Received': {}, 'FP_Taken': {}, 'Interviewed': {}, 'RFE': {}, 'Transferred': {},
                    'Approved': {}, 'Rejected': {}, "Pending": {}, 'Other': {}}
    for case_i in case_qs:
        if case_i.status in rd_status:
            status_l = "New"
        else:
            status_l = get_l_status(case_i.status, "L2")
            if status_l != "Pending":
                status_l = get_l_status(case_i.status, "L3")

        action_date = case_i.action_date_x.strftime("%m-%d-%Y")

        rn = int(case_i.receipt_number[3:])
        range_key = c_code + str(rn - (rn % rn_range))
        if range_key not in range_ls: range_ls.append(range_key)

        if range_key not in status_count[status_l]:
            status_count[status_l][range_key] = {date_ls[i]: 0 for i in range(60)}

        if action_date in date_ls:
            status_count[status_l][range_key][action_date] += 1

    for status_i in status_count:
        for range_key_i in range_ls:
            if range_key_i not in status_count[status_i]:
                status_count[status_i][range_key_i] = {date_ls[i]: 0 for i in range(60)}

    data_dict = {"status_count": status_count, "range_ls": range_ls[::-1], "date_ls": date_ls}

    with open(file_name, "w") as json_file:
        json.dump(data_dict, json_file)

    return data_dict


def get_nextstatus(center, formtype, curstat, statuslvl, daterange):
    next_status = {}
    to_endstatus = []

    ## Check the request from NextStatus(L1NS,L2NS,...) page or myCase("L1","L2",...) page
    ## if from NextStatus page the "curstat" is already transferred to the level
    ## set the "curstatuslvl" to "L0", it will keep the raw "curstat"
    if statuslvl[-2:]=="NS":
        curstatuslvl = "L0"
    else:
        curstatuslvl = statuslvl
    statuslvl = statuslvl[:-2]

    l4_name = get_l_status(curstat, "L4")
    if l4_name == "Final":
        next_status["Final"] = [0]
        data_dict = {"next_status": next_status, "to_endstatus": to_endstatus}
        return data_dict

    today = datetime.today()
    if daterange == "past3m":
        date_s = today + timedelta(days=-90)
    elif daterange == "past6m":
        date_s = today + timedelta(days=-180)
    elif daterange == "past9m":
        date_s = today + timedelta(days=-270)
    elif daterange == "past12m":
        date_s = today + timedelta(days=-365)
    elif daterange == "thisfy":
        if today.month > 9:
            date_s = date(today.year,10,1)
        else:
            date_s = date(today.year-1, 10, 1)


    if formtype == "":
        data_dict = {"formempty": []}
        return data_dict

    center_table = center_dict[center.lower()]
    # print(datetime.now())
    case_qs = center_table.objects.filter(form=formtype, action_date_x__gte=date_s).order_by("add_date")
    all_status = {}
    for case_i in case_qs:
        if case_i.action_date_x == date(2022, 9, 25) and case_i.action_date == "": continue
        if case_i.receipt_number not in all_status:
            all_status[case_i.receipt_number] = [case_i]
        else:
            all_status[case_i.receipt_number].append(case_i)

    for rn_i in all_status:
        rn_i_n = len(all_status[rn_i])
        if rn_i_n <= 1: continue
        for sn_i in range(rn_i_n):
            status_i = all_status[rn_i][sn_i].status
            status_i_l = get_l_status(status_i, statuslvl)
            mycase_status_l = get_l_status(curstat, curstatuslvl)
            # print(mycase_status_l)

            if status_i_l == mycase_status_l and (sn_i + 1) < rn_i_n: # and rn_i_status_date == "":
                ## Adding this: rn_i_status_date=="" to above only saving the first pair of status change.
                rn_i_status_date = all_status[rn_i][sn_i].action_date_x
                next_s = get_l_status(all_status[rn_i][sn_i + 1].status, statuslvl)
                next_s_days = (all_status[rn_i][sn_i + 1].action_date_x - rn_i_status_date).days
                if next_s_days <= 0: continue
                if next_s not in next_status:
                    next_status[next_s] = [next_s_days]
                else:
                    next_status[next_s].append(next_s_days)

                if get_l_status(all_status[rn_i][sn_i + 1].status, "L4") == "Final":
                    tofinal_days = (all_status[rn_i][sn_i+1].action_date_x - rn_i_status_date).days
                    if tofinal_days > 0:
                        to_endstatus.append(tofinal_days)

    # print(datetime.now())
    # for status_i in next_status:
    #     x_len = len(next_status[status_i])
    #     x_avg = int(sum(next_status[status_i]) / x_len)
    #     x_mid = np.median(next_status[status_i])
    #     x_min = min(next_status[status_i])
    #     x_max = max(next_status[status_i])
    #     next_status[status_i] = [x_len, x_avg, x_mid, x_min, x_max]
    if(len(to_endstatus))!=0:
        pass
        # to_endstatus = [int(sum(to_endstatus) / len(to_endstatus)), np.median(to_endstatus), min(to_endstatus), max(to_endstatus)]
    else:
        to_endstatus = []
    # print(next_status,to_endstatus)
    data_dict = {"next_status": next_status, "to_endstatus": to_endstatus}

    return data_dict
