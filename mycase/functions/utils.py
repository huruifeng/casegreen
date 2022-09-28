## Function library
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup
import re

from ctrlpanel.functions.utils import get_status_dict

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
center_names = ["MSC",	"LIN","SRC", "WAC", "EAC", "IOE", "YSC"]

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

status_dict = get_status_dict()

def get_status(recepit_number):
    ## Test
    # recepit_number="LIN2290104917"

    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    case_data = {"appReceiptNum": recepit_number}

    try_n = 0
    while True:
        ## Try N times at most
        resp = requests.post(url, data=case_data)
        try_n += 1
        if resp.status_code in [200]:
            break
        else:
            if try_n >=10:
                return ["try_failed"]

    soup = BeautifulSoup(resp.text, 'html.parser')
    status_div=soup.find("div",class_="rows text-center")
    if status_div:
        ## case exists
        status_h_text = status_div.h1.get_text(strip=True)
        if status_h_text.strip() == "":
            return ["error", "invlid_num"]

        status_p_text = status_div.p.get_text()
        status_p_text_ls = re.split(" |,", status_p_text)
        status_p_text_ls = [i for i in status_p_text_ls if i]

        date=""
        form=""
        n_words = len(status_p_text_ls)
        for i in range(n_words):
            if status_p_text_ls[i] in months:
                date = status_p_text_ls[i] + " " + status_p_text_ls[i+1]+", " + status_p_text_ls[i+2]
            elif status_p_text_ls[i] == "Form":
                form = status_p_text_ls[i+1]
                break
        if form == "":
            for form_x in form_types:
                if form_x in status_p_text:
                    form = form_x
                    break
        if date!="":
            status_p_text = status_p_text.replace(date, "<u>"+date+"</u>")
        if form!="":
            status_p_text = status_p_text.replace(form, "<u>"+form+"</u>")

        status_p_text = status_p_text.replace(recepit_number, "<u>"+recepit_number+"</u>")
        return [form, date,status_h_text,status_p_text]
    else:
        ## the case number is invlid
        return ["error","invlid_num"]

def get_l_status(status_str, l="L3"):
    if l== "L0": return status_str
    if status_str in status_dict:
        l_name = status_dict[status_str][l.upper()]
    else:
        l_name = "Other"
    return  l_name

def getcase_in_range(case_range,center,case_range_base,center_table,form_type,receipt_num):
    if case_range == "rn_range":
        case_range_s = center + str(case_range_base)
        case_range_e = center + str(case_range_base + 4999)
        case_qs = center_table.objects.filter(form=form_type,receipt_number__range=(case_range_s, case_range_e))
    elif case_range == "rn_n200":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:201]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_n500":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:501]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_n1000":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:1001]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_p200":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:201]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_p500":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:501]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_p1000":
        case_range_s = receipt_num
        case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:1001]]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
    elif case_range == "rn_np200":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:200]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:201]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rn_np500":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:500]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:501]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rn_np1000":
        case_range_s = receipt_num
        case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
        case_qs1 = case_qs1.order_by("-receipt_number")[:1000]
        case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
        case_qs2 = case_qs2.order_by("receipt_number")[:1001]
        case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
        case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs)
        del case_qs1
        del case_qs2
    elif case_range == "rd_n1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-30)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
        else:
            case_qs = []
    elif case_range == "rd_n2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-60)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
        else:
            case_qs = []
    elif case_range == "rd_n3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-90)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd.rd_date))
        else:
            case_qs = []
    elif case_range == "rd_p1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+30)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
        else:
            case_qs = []
    elif case_range == "rd_p2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+60)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
        else:
            case_qs = []
    elif case_range == "rd_p3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_e = case_rd.rd_date + timedelta(days=+90)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date, case_rd_e))
        else:
            case_qs = []
    elif case_range == "rd_np1m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-30)
            case_rd_e = case_rd.rd_date + timedelta(days=+30)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
        else:
            case_qs = []
    elif case_range == "rd_np2m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-60)
            case_rd_e = case_rd.rd_date + timedelta(days=+60)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
        else:
            case_qs = []
    elif case_range == "rd_np3m":
        case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
        if case_rd.rd_date != date(2000, 1, 1):
            case_rd_s = case_rd.rd_date + timedelta(days=-90)
            case_rd_e = case_rd.rd_date + timedelta(days=+90)
            case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s, case_rd_e))
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

def casestatus(date_range,center_table,form_type,receipt_num):
    all_status = {}
    pass

def get_daily_counts(center_table,form_type):
    counts_qs = center_table.objects.filter()