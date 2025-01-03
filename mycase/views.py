import json
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from mycase.functions.utils import *
from mycase.models import *

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

color20 = {'Received': '#1266f1', 'Transferred': '#17becf', 'Pending': '#ff7f0e',
           'FP_Scheduled': '#1f77b4', 'FP_Taken': '#aec7e8', 'InterviewScheduled': '#9467bd',
           'InterviewCompleted': '#c5b0d5','RFE_Sent': '#bcbd22', 'RFE_Received': '#dbdb8d',
           'Approved': '#2ca02c', 'Produced': '#98df8a','Mailed': '#a1d99b',
           'Hold': '#ffbb78', 'ReturnHold': '#8c564b', 'NoticeSent': '#c49c94', 'Reopened': '#e377c2',
           'Other': '#f7b6d2','Rejected': '#d62728', 'Terminated': '#ff9896',
           'bk1': '#7f7f7f', 'bk2': '#c7c7c7', 'bk3': '#9edae5'}

color8 = {'Received': "#1072f1", 'FP_Taken': "#11a9fa", 'Interviewed': "#2b04da", 'RFE': "#f4b824",
          'Transferred': "#c77cff", 'Approved': "#1db063", 'Rejected': "#ff001a", 'Other': "#78787a"}

# rd_status = ["Fees Were Waived", "Card Was Received By USCIS Along With My Letter", "Case Accepted By The USCIS Lockbox",
#              "Case Was Received", "Case Was Received and A Receipt Notice Was Sent", "Case Was Received At Another USCIS Office",
#              "Document and Letter Was Received", "Document And Letter Was Received And Under Review",
#              "Fingerprint Fee Was Received","Immigrant Visa Fee Payment Received"]

rd_status = get_rd_status()

def index(request):
    return render(request, 'index.html')

def mycase(request):
    if request.method == "GET":
        receipt_num = request.GET.get("receipt_number", None)
    elif request.method == "POST":
        receipt_num = request.POST.get("receipt_number", None)

    if receipt_num is None or receipt_num.strip() == "":
        return redirect("casegreen:home")

    receipt_num = receipt_num.strip()
    center = receipt_num[:3]
    year = receipt_num[3:5]
    lb_sc = "LB" if receipt_num[5] == "9" else "SC"

    ## try to get real-time data from uscis
    try:
        status_ls = get_status(receipt_num)
        # print(status_ls)
    except Exception as e:
        # print(e)
        status_ls = []

    ## read exist data from database
    if center.upper()=="IOE":
        center_table = case_status_ioe
    else:
        center_table = center_dict[center.lower() + "_" + lb_sc.lower()]
    status_qs = center_table.objects.filter(receipt_number=receipt_num)
    if status_qs.exists():
        status_qs = status_qs.order_by("add_date")
        if len(status_ls) >= 3:
            try:
                time_x = datetime.strptime(status_ls[1], "%B %d, %Y").date()
            except Exception as e:
                time_x = datetime.now().date()

            days = (datetime.now().date() - time_x).days
            if status_ls[0] == "":
                status_ls[0] = status_qs.last().form
            if status_qs.last().status != status_ls[2]:
                l3_name = get_l_status(status_ls[2], "L3")

                if l3_name in ["Approved"]:
                    case_stage = "Approved"
                elif l3_name in ["Rejected"]:
                    case_stage = "Rejected"
                elif l3_name in ["RFE"]:
                    case_stage = "RFE"
                else:
                    case_stage = "Processing"

                new_status = center_table.objects.create(receipt_number=receipt_num,
                                                         form=status_ls[0],
                                                         status=status_ls[2],
                                                         action_date=status_ls[1],
                                                         action_date_x=time_x,
                                                         case_stage=case_stage,
                                                         add_date=datetime.now(),
                                                         date_number=(datetime.now() - datetime(2000, 1, 1)).days)
                new_status.save()
                status_qs = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")
            else:
                pass
        else:
            status_ls = [status_qs.last().form, status_qs.last().action_date_x, status_qs.last().status, ""]
            time_x = status_qs.last().action_date_x
            days = (datetime.now().date() - time_x).days
    else:
        if len(status_ls) < 3:
            status_ls = ["NA", "NA", "Cannot get the data!", ""]
            days = "NA"
        else:
            ## Case is valid but does not exist in database
            if receipt_num.startswith("IOE"):
                with open("mycase/data/crawler/ioetoadd/" + receipt_num, 'w') as fp:
                    pass

            time_x = datetime.strptime(status_ls[1], "%B %d, %Y")
            days = (datetime.now() - time_x).days
            l3_name = get_l_status(status_ls[2], "L3")

            rd_date = date(2000, 1, 1)
            fy_x = 2000
            if status_ls[2] in rd_status:
                rd_date = time_x
                fy_x = rd_date.year
                if rd_date.month > 9: fy_x += 1
            else:
                if receipt_num.startswith("IOE"):
                    pass
                else:
                    fy_x =int(receipt_num[3:5])+2000

            if l3_name in ["Approved"]:
                case_stage = "Approved"
            elif l3_name in ["Rejected"]:
                case_stage = "Rejected"
            elif l3_name in ["RFE"]:
                case_stage = "RFE"
            else:
                case_stage = "Processing"

            new_status = center_table.objects.create(receipt_number=receipt_num,
                                                     form=status_ls[0],
                                                     status=status_ls[2],
                                                     action_date=status_ls[1],
                                                     action_date_x=time_x,
                                                     case_stage=case_stage,
                                                     add_date=datetime.now(),
                                                     date_number=(datetime.now() - datetime(2000, 1, 1)).days,
                                                     rd_date=rd_date,
                                                     fiscal_year=fy_x)
            new_status.save()
            status_qs = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")

    case_range_s = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)
    case_range_e = case_range_s + 4999

    form_ls = []
    if status_ls[0] == "":
        ## form type is not available
        form_qs = form.objects.all()
        form_ls = [form_i.code for form_i in form_qs]

    context = {
        "status": {'form': status_ls[0], 'date': status_ls[1], 'status': status_ls[2], 'status_text': status_ls[3],"days": days},
        "receipt_num": receipt_num, "case_range": str(case_range_s) + "-" + str(case_range_e), "form_ls": form_ls,
        "status_qs": status_qs, "page_title": "myCase"}
    return render(request, 'mycase/mycase.html', context)


def caseinrange(request):
    # request should be ajax and method should be GET.
    if request.method == "GET":
        # get the data_type from the client side.
        receipt_num = request.GET.get("recepit_num", None)
        form_type = request.GET.get("form_type", None)
        case_range = request.GET.get("case_range", None)
        selectform = request.GET.get("selectform", None)

        delta_1d = datetime.today().date() + timedelta(days=-2)
        delta_1w = datetime.today().date() + timedelta(days=-8)
        delta_2w = datetime.today().date() + timedelta(days=-15)

        if form_type == "":
            data_dict = {"n_cases": 0, "message": "Form type is not available!"}
            return JsonResponse(data_dict, status=200)

        # check for the data_type.
        if receipt_num is not None:
            center = receipt_num[:3]
            year = receipt_num[3:5]
            lb_sc = "LB" if receipt_num[5] == "9" else "SC"
            if center.upper() == "IOE":
                center_table = case_status_ioe
            else:
                center_table = center_dict[center.lower() + "_" + lb_sc.lower()]

            if selectform == "yes" and form_type != "":
                case_x = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date").first()
                case_x.form = form_type
                case_x.save()

            case_range_base = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)
            case_qs = getcase_in_range(case_range, center, case_range_base, center_table, form_type, receipt_num)

            ##########
            # print(len(case_qs))
            if len(case_qs) > 0:
                status_letter = {"Received": "R", "FP_Taken": "F", "Interviewed": "I", "RFE": "E", "Transferred": "T",
                                 "Approved": "A", "Rejected": "J", "Other": "O"}
                status_abbr = {"Received": "REC", "FP_Taken": "FP", "Interviewed": "ITV", "RFE": "RFE",
                               "Transferred": "TRF", "Approved": "APV", "Rejected": "RJC", "Other": "OTH"}

                status_counts = {"Received": 0, "FP_Taken": 0, "Interviewed": 0, "RFE": 0, "Transferred": 0,
                                 "Approved": 0, "Rejected": 0, "Other": 0}
                status_1d = {"Received": 0, "FP_Taken": 0, "Interviewed": 0, "RFE": 0, "Transferred": 0, "Approved": 0,
                             "Rejected": 0, "Other": 0}
                status_1w = {"Received": 0, "FP_Taken": 0, "Interviewed": 0, "RFE": 0, "Transferred": 0, "Approved": 0,
                             "Rejected": 0, "Other": 0}
                status_2w = {"Received": 0, "FP_Taken": 0, "Interviewed": 0, "RFE": 0, "Transferred": 0, "Approved": 0,
                             "Rejected": 0, "Other": 0}

                status_seq = ""
                status_mut = []
                status_dom = []
                i = 0
                used_case = []
                mystatus_l3 = ""
                mypos = -1
                for case_i in case_qs.order_by("receipt_number", "-add_date"):
                    if case_i.receipt_number in used_case:
                        continue
                    else:
                        used_case.append(case_i.receipt_number)

                    ####
                    i += 1
                    l3_name = get_l_status(case_i.status, "L3")

                    status_counts[l3_name] += 1
                    if case_i.action_date_x >= delta_1d:
                        status_1d[l3_name] += 1
                    if case_i.action_date_x >= delta_1w:
                        status_1w[l3_name] += 1
                    if case_i.action_date_x >= delta_2w:
                        status_2w[l3_name] += 1

                    status_seq += status_letter[l3_name]
                    if case_i.receipt_number == receipt_num:
                        status_mut.append(
                            {"ID": case_i.receipt_number, "Num": 1.5, "POS": i, "STATUS": status_abbr[l3_name],
                             "ACTDATE": case_i.action_date_x})
                        mystatus_l3 = l3_name
                        mypos = status_counts[l3_name]
                    else:
                        status_mut.append(
                            {"ID": case_i.receipt_number, "Num": 1, "POS": i, "STATUS": status_abbr[l3_name],
                             "ACTDATE": case_i.action_date_x})
                    status_dom.append({"ID": status_abbr[l3_name], "START": i - 0.5, "END": i + 0.5})
                n_cases = len(used_case)

                ## merge doamin:
                status_dom_merged = [{"ID": "", "START": 0, "END": len(case_qs) + 1}]
                ID_prev = status_dom[0]["ID"]
                start_i = status_dom[0]["START"]
                for i in range(1, len(status_dom)):
                    if status_dom[i]["ID"] != ID_prev:
                        status_dom_merged.append({"ID": ID_prev, "START": start_i, "END": status_dom[i]["START"]})
                        ID_prev = status_dom[i]["ID"]
                        start_i = status_dom[i]["START"]
                status_dom_merged.append({"ID": ID_prev, "START": start_i, "END": status_dom[i]["END"]})

                for status_i in ["Received", "FP_Taken", "Interviewed", "RFE", "Transferred", "Approved", "Rejected",
                                 "Other"]:
                    if status_i == mystatus_l3:
                        break
                    else:
                        mypos += status_counts[status_i]
                pre_apv_poll = n_cases - status_counts["Other"] - status_counts["Rejected"] - status_counts["Approved"]

                if mystatus_l3 in ["Received", "FP_Taken", "Interviewed", "RFE", "Transferred"]:
                    mypos_text = "YOU are approaching...(" + str(mypos) + "/" + str(
                        pre_apv_poll) + ") <i class='fas fa-fighter-jet'></i>"
                elif mystatus_l3 in ["Approved"]:
                    mypos_text = "Congrats! <i class='fas fa-glass-cheers'></i>"
                else:
                    mypos_text = "YOU"

                mypos = round(mypos / n_cases * 100.0)
                ####################
                used_case = []
                recent_apv = {}
                recent_trf = {}
                recent_rfe = {}
                for case_i in case_qs.order_by("-action_date_x"):  ## here also can use "-add_date"
                    ## open the comments, only count the final status of a receipt number(one case can have several status changes within a few days)
                    # if case_i.receipt_number in used_case: continue
                    # else: used_case.append(case_i.receipt_number)

                    l3_name = get_l_status(case_i.status, "L3")
                    if l3_name == "Approved" and len(recent_apv) < 5: recent_apv[
                        case_i.receipt_number] = case_i.action_date_x
                    if l3_name == "Transferred" and len(recent_trf) < 5: recent_trf[
                        case_i.receipt_number] = case_i.action_date_x
                    if l3_name == "RFE" and len(recent_rfe) < 5: recent_rfe[
                        case_i.receipt_number] = case_i.action_date_x
                    if len(recent_apv) + len(recent_trf) + len(recent_rfe) >= 15: break

                del used_case[:]
                data_dict = {"n_cases": n_cases, "status_counts": list(status_counts.values()),
                             "status_1d": status_1d, "status_1w": status_1w, "status_2w": status_2w,
                             "recent_apv": recent_apv, "recent_trf": recent_trf, "recent_rfe": recent_rfe,
                             "mypos": mypos, "mypos_text": mypos_text,
                             "status_seq": status_seq, "status_mut": status_mut, "status_dom": status_dom_merged}
                return JsonResponse(data_dict, status=200)
            else:  ## queryset is empty
                data_dict = {"n_cases": 0, "message": "No data is recorded for this option!"}
                return JsonResponse(data_dict, status=200)
        else:  ## receipt_num is None
            data_dict = {"n_cases": 0, "message": "Bad request of Recepit/Case number!"}
            return JsonResponse(data_dict, status=200)
    else:  ## ajax, GET error
        data_dict = {"n_cases": 0, "message": "Request error!"}
        return JsonResponse(data_dict, status=200)


def mynextstatus(request):
    mycase_status = request.GET.get("mystatus", None)
    daterange = request.GET.get("daterange", None)
    formtype = request.GET.get("form_type", None)
    statuslvl = request.GET.get("status_level", None)
    receipt_num = request.GET.get("recepit_num", None)

    selectform = request.GET.get("selectform", None)
    if receipt_num is not None:
        center = receipt_num[:3]
        if center.upper() == "IOE":
            center_table = case_status_ioe
        else:
            lb_sc = "LB" if receipt_num[5] == "9" else "SC"
            center = center.lower() + "_" + lb_sc.lower()
            center_table = center_dict[center]
        if selectform == "yes" and formtype != "":
            case_x = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date").first()
            case_x.form = formtype
            case_x.save()
    else:
        pass

    data_dict = get_nextstatus(center,formtype,mycase_status,statuslvl,daterange)
    return JsonResponse(data_dict, status=200)

def dailyrecords(request):
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)

    if selectform is None or center is None:
        data_dict = {"label_ls": [], "count_ls": []}
        return JsonResponse(data_dict, status=200)

    data_dict = get_dailyrecords(center, selectform)
    return JsonResponse(data_dict, status=200)


def dashbordajax(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

    context = {"page_title": "Dashbord", "form_ls": form_ls}
    return render(request, 'mycase/dashbordajax.html', context)


def dashborddaily(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)

    if selectform is None or center is None:
        return redirect("/dashborddaily?center=LIN_LB&selectform=I-485", status=200)

    data_dict = get_dailyrecords(center, selectform)

    context = {"page_title": "Dashbord daily", "form_ls": form_ls, "chart_data": data_dict, "center": center,
               "selectform": selectform}
    return render(request, 'mycase/dashborddaily.html', context)


def rnrangecount(request):
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        statuslevel = request.GET.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        statuslevel = request.POST.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None:
        data_dict = {"dataset": 0, "label": []}
        return JsonResponse(data_dict, status=200)

    center_table = center_dict[center.lower()]
    data_dict = get_rnrangecount(center_table, center, selectform, fy, statuslevel, rangesize)

    return JsonResponse(data_dict, status=200)


def processrn(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        statuslevel = request.GET.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        statuslevel = request.POST.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None or statuslevel is None or rangesize is None:
        return redirect(
            "/processrn?center=LIN_LB&selectform=I-485&fy=" + str(now.year) + "&statuslevel=L3&rangesize=5000",
            status=200)

    center_table = center_dict[center.lower()]
    data_dict = get_rnrangecount(center_table, center, selectform, fy, statuslevel, rangesize)

    context = {"page_title": "Case range process", "form_ls": form_ls, "year_ls": year_ls[::-1],
               "chart_data": json.dumps(data_dict),
               "center": center, "fy": fy, "selectform": selectform, "statuslevel": statuslevel, "rangesize": rangesize}
    return render(request, 'mycase/processrn.html', context)


def processrd(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        statuslevel = request.GET.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        statuslevel = request.POST.get("statuslevel", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None or statuslevel is None or rangesize is None:
        return redirect(
            "/processrd?center=LIN_LB&selectform=I-485&fy=" + str(now.year) + "&statuslevel=L3&rangesize=weekly",
            status=200)

    center_table = center_dict[center.lower()]
    data_dict = get_rdcount(center_table, center, selectform, fy, statuslevel, rangesize)

    context = {"page_title": "Case range process", "form_ls": form_ls, "year_ls": year_ls[::-1],
               "chart_data": json.dumps(data_dict),
               "center": center, "fy": fy, "selectform": selectform, "statuslevel": statuslevel, "rangesize": rangesize}
    return render(request, 'mycase/processrd.html', context)


def processajax(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    context = {"page_title": "Case range process", "form_ls": form_ls, "year_ls": year_ls[::-1], }
    return render(request, 'mycase/processajax.html', context)


def getsankey(request):
    center = request.GET.get("center", None)
    selectform = request.GET.get("selectform", None)
    statuslevel = request.GET.get("statuslevel", None)

    days = 8
    date_ls = status_trans.objects.order_by('-action_date').values('action_date').distinct()[:days][::-1]

    status_trans_dict = {}
    date_str_ls = []

    source_date = date_ls[0]["action_date"].strftime("%m-%d-%Y")
    for d_i in range(1,days):
        date_i = date_ls[d_i]["action_date"]
        trans_qs = status_trans.objects.filter(center=center, form_type=selectform, action_date=date_i)

        dest_date = date_i.strftime("%m-%d-%Y")
        date_str_ls.append(source_date)

        status_trans_dict[dest_date] = {}
        for trans_i in trans_qs:
            source_s = trans_i.source_status
            dest_s = trans_i.dest_status

            ## Only show the changed records
            if source_s == dest_s: continue
            if source_s == "no_yesterday": continue

            source_s_l = source_date + ":" + get_l_status(source_s, statuslevel)
            dest_s_l = dest_date + ":" + get_l_status(dest_s, statuslevel)

            if source_s_l in status_trans_dict[dest_date]:
                if dest_s_l in status_trans_dict[dest_date][source_s_l]:
                    status_trans_dict[dest_date][source_s_l][dest_s_l] += trans_i.count
                else:
                    status_trans_dict[dest_date][source_s_l][dest_s_l] = trans_i.count
            else:
                status_trans_dict[dest_date][source_s_l] = {dest_s_l: trans_i.count}
        source_date = dest_date

    date_str_ls.append(dest_date)
    # print(date_str_ls)

    node_ls = []
    link_ls = []
    for date_i in status_trans_dict:
        for source_i in status_trans_dict[date_i]:
            for dest_i in status_trans_dict[date_i][source_i]:
                link_ls.append({"action_date": date_i, "source": source_i, "target": dest_i,
                                "value": status_trans_dict[date_i][source_i][dest_i]})

                date_i_depth = date_str_ls.index(source_i[:10])
                node_i = {"name": source_i, "depth": date_i_depth}
                if node_i not in node_ls: node_ls.append(node_i)

                date_i_depth = date_str_ls.index(dest_i[:10])
                node_i = {"name": dest_i, "depth": date_i_depth}
                if node_i not in node_ls: node_ls.append(node_i)

    # data_dict = {"sankey":status_trans_dict}
    data_dict = {"nodes": node_ls, "links": link_ls}
    return JsonResponse(data_dict, status=200)


def overview(request):
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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        fy = request.GET.get("fy", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        fy = request.POST.get("fy", None)

    if center is None or fy is None:
        return redirect("/overview?center=LIN_LB&fy=" + str(now.year), status=200)

    form_status_count = {}
    file_name = "_".join([center.upper(), fy[-2:]]) + ".json"
    folder = "mycase/data/statistics/overview"
    file_name = folder + "/" + file_name
    while True:
        if os.path.exists(file_name):
            try:
                with open(file_name) as json_file:
                    form_status_count = json.load(json_file)
                break
            except Exception as e:
                print(e)
        else:
            ok = overview_x(center, fy)
            if "Error" in ok:
                break

    context = {"page_title": "Overview", "year_ls": year_ls[::-1], "center": center, "fy": fy,
               "form_status_count": form_status_count}
    return render(request, 'mycase/overview.html', context)


def todaycounts(request):
    ##center_running
    center_running_latest = center_running.objects.all().order_by("-start").first()
    last_date = center_running_latest.start
    last_date = (last_date + timedelta(days=-1))

    if request.method == "GET":
        data_date_str = request.GET.get("data_date", None)

    if data_date_str is None:
        data_date_str = last_date.date().strftime("%m-%d-%Y")
        return redirect("/today?data_date=" + data_date_str, status=200)

    data_date = datetime.strptime(data_date_str, "%m-%d-%Y")
    date_num = (data_date - datetime(2000, 1, 1)).days + 1

    today_count = {}
    for center_i in center_dict:
        today_count[center_i.upper()] = get_dailyrecords(center=center_i, selectform="", date_number=date_num)
    ytd_count = get_ytdcount(data_date)

    form_ls = []
    for center_i in ytd_count:
        for form_i in ytd_count[center_i]:
            if form_i not in form_ls: form_ls.append(form_i)
            if center_i not in today_count:
                ytd_count[center_i][form_i] = {**ytd_count[center_i][form_i],
                                               **{"rec_d": 0, "fp_d": 0, "itv_d": 0, "rfe_d": 0, "trf_d": 0, "apv_d": 0,
                                                  "rej_d": 0, "pending_d": 0, "oth_d": 0}}
            else:
                if form_i not in today_count[center_i]:
                    ytd_count[center_i][form_i] = {**ytd_count[center_i][form_i],
                                                   **{"rec_d": 0, "fp_d": 0, "itv_d": 0, "rfe_d": 0, "trf_d": 0,
                                                      "apv_d": 0, "rej_d": 0, "pending_d": 0, "oth_d": 0}}
                else:
                    ytd_count[center_i][form_i] = {**ytd_count[center_i][form_i], **today_count[center_i][form_i]}

    if data_date.month >= 10:
        fy = data_date.year + 1
    else:
        fy = data_date.year

    fy_end = datetime(fy+1, 9, 30)
    fy_end = data_date_str if fy_end > datetime.now() else "09-30"+"-"+str(fy+1)

    show_form_ls = ["I-485", "I-140", "I-765", "I-131", "I-129", "I-539", "I-130"]
    last_date = last_date.date().strftime("%m-%d-%Y")
    context = {"page_title": "Today!", "ytd_count": ytd_count, "data_date": data_date_str, "last_date":last_date,
               "fy": fy,"fy_end":fy_end,"show_form_ls": show_form_ls, "form_ls": form_ls}
    return render(request, 'mycase/today.html', context)


def todaymodalcasetable(request):
    center_form_status = request.GET.get("center_form_status", None)
    picked_date = request.GET.get("picked_date", None)

    error_msg = ""
    if center_form_status is not None:
        center, form, status = center_form_status.split(":")
    else:
        error_msg = "Center/Form/Status is not defined!"

    if picked_date is not None:
        picked_date = datetime.strptime(picked_date, "%m-%d-%Y")
        picked_days = (picked_date - datetime(2000, 1, 1)).days + 1
    else:
        error_msg = "Date is not defined!"

    center_obj = center_dict[center.lower()]
    case_qs = center_obj.objects.filter(date_number=picked_days,form=form)

    status_map = {"new": rd_status, "apv": ["Approved", "Mailed", "Produced"], "rej": ["Rejected"]}
    case_qs_final = []
    for case_i in case_qs:
        l_status = case_i.status if status == "new" else get_l_status(case_i.status, "L2")
        if l_status in status_map[status]:
            case_qs_final.append([case_i.receipt_number, case_i.form, case_i.status, case_i.action_date,case_i.add_date.date()])

    data_dict = {"center": center, "case_qs": case_qs_final, "error_msg": error_msg}
    return JsonResponse(data_dict, status=200)

def countscalendar(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None or rangesize is None:
        return redirect("/countscalendar?center=LIN_LB&selectform=I-485&fy=" + str(now.year) + "&rangesize=5000",status=200)

    count_data = get_rangestatuscount(center,fy, selectform,rangesize)

    context = {"page_title": "Count calendar", "form_ls": form_ls, "year_ls": year_ls[::-1],
               "chart_data": json.dumps(count_data), "center": center, "fy": fy, "selectform": selectform, "rangesize": rangesize}
    return render(request, 'mycase/countscalendar.html', context)

def nextstatus(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        statuslevel = request.GET.get("statuslevel", None)
        daterange = request.GET.get("daterange", None)
        cursta = request.GET.get("cursta", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        statuslevel = request.POST.get("statuslevel", None)
        daterange = request.GET.get("daterange", None)
        cursta = request.GET.get("cursta", None)

    if center is None or selectform is None or statuslevel is None or daterange is None or cursta is None:
        return redirect("/nextstatus?center=MSC_LB&selectform=I-485&statuslevel=L0NS&daterange=past3m&cursta=Case Was Received",status=200)

    status_lvl_ls = get_status_list()
    data_dict = get_nextstatus(center, selectform, cursta, statuslevel, daterange)
    context = {"page_title": "NextStatus!",  "form_ls": form_ls, "status_lvl_ls":status_lvl_ls, "data":data_dict,
               "center": center, "selectform": selectform, "statuslevel":statuslevel, "daterange": daterange,"cursta":cursta}
    return render(request, 'mycase/nextstatus.html', context)

def get_status_list():
    case_status_df = pd.read_csv("mycase/data/case_status.csv", header=0, index_col=None, sep=",")
    status_lvl_ls = case_status_df.to_dict(orient="list")
    status_lvl_ls = {k:sorted(set(status_lvl_ls[k])) for k in status_lvl_ls}
    return status_lvl_ls

def summaryrn(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None or rangesize is None:
        return redirect("/summaryrn?center=LIN_LB&selectform=I-485&fy=" + str(now.year) + "&rangesize=5000",status=200)

    center_table = center_dict[center.lower()]
    data_dict = get_rnrangesummary(center_table, center, selectform, fy, rangesize)

    context = {"page_title": "Summary by Receipt Number","form_ls": form_ls, "year_ls": year_ls[::-1],
               "center": center, "fy": fy, "selectform": selectform,"rangesize": rangesize,"data":data_dict}
    return render(request, 'mycase/summaryrn.html', context)

def summaryrd(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

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

    ######
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("selectform", None)
        fy = request.GET.get("fy", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("selectform", None)
        fy = request.POST.get("fy", None)
        rangesize = request.GET.get("rangesize", None)

    if selectform is None or center is None or fy is None or rangesize is None:
        return redirect("/summaryrd?center=LIN_LB&selectform=I-485&fy=" + str(now.year) + "&rangesize=weekly",status=200)

    center_table = center_dict[center.lower()]
    data_dict = get_rdsummary(center_table, center, selectform, fy, rangesize)

    context = {"page_title": "Summary by Receipt Date","form_ls": form_ls, "year_ls": year_ls[::-1],
               "center": center, "fy": fy, "selectform": selectform,"rangesize": rangesize,"data":data_dict}
    return render(request, 'mycase/summaryrd.html', context)


def queryrn(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]
    context = {"page_title": "Query by RN","form_ls": form_ls,"selectform": "I-485","rangesize": "500",}
    return render(request, 'mycase/queryrn.html', context)

def ajax_queryrn(request):
    if request.method == "GET":
        receipt_num = request.GET.get("receipt_num", None)
        selectform = request.GET.get("selectform", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        receipt_num = request.POST.get("receipt_num", None)
        selectform = request.POST.get("selectform", None)
        rangesize = request.GET.get("rangesize", None)

    if receipt_num is None or len(receipt_num.strip())!=13 or (receipt_num.strip()[:3] not in ['LIN','SRC','MSC','WAC','EAC','YSC','IOE','MCT']):
        data_dict = {"data":"Error: Receipt number format is wrong!"}
        return JsonResponse(data_dict, status=200)

    receipt_num = receipt_num.strip()

    center = receipt_num[:3]
    year = receipt_num[3:5]
    lb_sc = "LB" if receipt_num[5] == "9" else "SC"

    receipt_num_pool = []
    for i in range(int(rangesize)):
        receipt_num_pool.append(center+str(int(receipt_num[3:])+i))

    if center.upper() == "IOE":
        center_table = center_dict[center.lower()]
    else:
        center_table = center_dict[center.lower() + "_" + lb_sc.lower()]
    # print(center_table)
    case_qs = center_table.objects.filter(form=selectform,receipt_number__in=receipt_num_pool).order_by("add_date")
    all_status = {}
    for case_i in case_qs:
        if case_i.receipt_number not in all_status:
            all_status[case_i.receipt_number] = [[case_i.status,case_i.action_date,case_i.case_stage]]
        else:
            all_status[case_i.receipt_number].append([case_i.status,case_i.action_date,case_i.case_stage])
    data_dict = {"data": all_status}
    return JsonResponse(data_dict, status=200)

def queryrd(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]
    context = {"page_title": "Query by RD", "form_ls": form_ls, "selectform": "I-485", "rangesize": "3", }
    return render(request, 'mycase/queryrd.html', context)

def ajax_queryrd(request):
    if request.method == "GET":
        center = request.GET.get("center", None)
        received_date = request.GET.get("received_date", None)
        selectform = request.GET.get("selectform", None)
        rangesize = request.GET.get("rangesize", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        received_date = request.POST.get("received_date", None)
        selectform = request.POST.get("selectform", None)
        rangesize = request.GET.get("rangesize", None)

    if received_date is None or len(received_date.strip())!=10 or center==None:
        data_dict = {"data":"Error: Received date format is wrong!"}
        return JsonResponse(data_dict, status=200)

    received_date = received_date.strip()

    date_s = datetime.strptime(received_date, "%m-%d-%Y")
    date_e = date_s + timedelta(days=30*int(rangesize))

    center_table = center_dict[center.lower()]
    case_qs = center_table.objects.filter(form=selectform,rd_date__range=(date_s,date_e)).order_by("add_date")
    all_status = {}
    for case_i in case_qs:
        if case_i.receipt_number not in all_status:
            all_status[case_i.receipt_number] = [[case_i.status,case_i.action_date,case_i.case_stage,case_i.rd_date]]
        else:
            all_status[case_i.receipt_number].append([case_i.status,case_i.action_date,case_i.case_stage,case_i.rd_date])
    data_dict = {"data": all_status}
    return JsonResponse(data_dict, status=200)


def about(request):
    center_counts = {}
    for center_i in center_dict:
        center_counts[center_i] = {"total":center_dict[center_i].objects.values('id').order_by("id").last()}

    context = {"page_title": "About","center_counts":center_counts}
    return render(request, 'mycase/about.html', context)

def comments(request):
    context = {"page_title": "Comments"}
    return render(request, 'mycase/comments.html', context)


def statuslist(request):
    status_dict = get_status_dict()
    context = {"page_title": "Status List","status_dict":status_dict}
    return render(request, 'mycase/statuslist.html', context)

