import json
from datetime import datetime, timedelta

from bottleneck import median
from django.db.models import Max, F
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from mycase.functions.utils import get_status, getcase_in_range, get_l_status
from mycase.models import *

# Create your views here.
center_dict = {"lin_lb":case_status_lin_lb,
               "msc_lb":case_status_msc_lb,
               "src_lb":case_status_src_lb,
               "wac_lb":case_status_wac_lb,
               "eac_lb":case_status_eac_lb,
               "ysc_lb":case_status_ysc_lb,
               "lin_sc":case_status_lin_sc,
               "msc_sc":case_status_msc_sc,
               "src_sc":case_status_src_sc,
               "wac_sc":case_status_wac_sc,
               "eac_sc":case_status_eac_sc,
               "ysc_sc":case_status_ysc_sc,
               "ioe":case_status_ioe
               }

color20 = {'Received':'#1266f1','Transferred':'#17becf','Pending':'#ff7f0e',
           'FP_Scheduled':'#1f77b4','FP_Taken':'#aec7e8','InterviewScheduled':'#9467bd','InterviewCompleted':'#c5b0d5',
           'RFE_Sent':'#bcbd22','RFE_Received':'#dbdb8d',  'Approved':'#2ca02c', 'Produced':'#98df8a','Mailed':'#a1d99b',
           'Hold':'#ffbb78','ReturnHold':'#8c564b','NoticeSent':'#c49c94','Reopened':'#e377c2','Other':'#f7b6d2',
           'Rejected':'#d62728', 'Terminated':'#ff9896','bk1':'#7f7f7f','bk2':'#c7c7c7','bk3':'#9edae5'}

color8 = {'Received':"#1072f1",'FP_Taken':"#11a9fa",'Interviewed': "#2b04da",'RFE':"#f4b824",
          'Transferred':"#c77cff",'Approved': "#1db063",'Rejected': "#ff001a",'Other':"#78787a"}
def index(request):
    return render(request,'mycase/index.html')

def mycase(request):
    if request.method == "GET":
        receipt_num = request.GET['receipt_number']
    elif request.method == "POST":
        receipt_num = request.POST['receipt_number']

    center = receipt_num[:3]
    year = receipt_num[3:5]
    lb_sc = "LB" if receipt_num[5]=="9" else "SC"

    ## try to get real-time data from uscis
    try:
        status_ls = get_status(receipt_num)
    except Exception as e:
        status_ls = []

    ## read exist data from database
    center_table = center_dict[center.lower()+"_"+ lb_sc.lower()]
    status_qs = center_table.objects.filter(receipt_number=receipt_num)
    if status_qs.exists():
        status_qs = status_qs.order_by("add_date")
        if len(status_ls) >= 3:
            try:
                time_x = datetime.strptime(status_ls[1], "%B %d, %Y").date()
            except Exception as e:
                time_x = datetime.now().date()

            days = (datetime.now().date() - time_x).days
            if status_ls[0]=="":
                status_ls[0] = status_qs.last().form
            if status_qs.last().status != status_ls[2]:
                l3_name = get_l_status(status_ls[2],"L3")

                if l3_name in ["Approved"]: case_stage = "Approved"
                elif l3_name in ["Rejected"]: case_stage = "Rejected"
                elif l3_name in ["RFE"]: case_stage = "RFE"
                else: case_stage = "Processing"

                new_status = center_table.objects.create(receipt_number =receipt_num,
                                            form = status_ls[0],
                                            status =status_ls[2],
                                            action_date =status_ls[1],
                                            action_date_x = time_x,
                                            case_stage=case_stage,
                                            add_date = datetime.now(),
                                            date_number = (datetime.now() - datetime(2000, 1, 1)).days)
                new_status.save()
                status_qs = center_table.objects.filter(receipt_number=receipt_num).order_by("add_date")
            else:
                pass
        else:
            status_ls = [status_qs.last().form,status_qs.last().action_date_x, status_qs.last().status, ""]
            time_x = datetime.strptime(status_qs.last().action_date, "%B %d, %Y")
            days = (datetime.now()-time_x).days
    else:
        if len(status_ls) < 3:
            status_ls = ["NA","NA", "Cannot get the data!", ""]
            days = "NA"
        else:
            time_x = datetime.strptime(status_ls[1], "%B %d, %Y")
            days = (datetime.now() - time_x).days
            l3_name = get_l_status(status_ls[2],"L3")

            if l3_name in ["Approved"]: case_stage = "Approved"
            elif l3_name in ["Rejected"]:case_stage = "Rejected"
            elif l3_name in ["RFE"]:case_stage = "RFE"
            else:case_stage = "Processing"

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

    case_range_s = int(receipt_num[3:]) - int(int(receipt_num[3:])%5000)
    case_range_e = case_range_s + 4999

    form_ls = []
    if status_ls[0] == "":
        ## form type is not available
        form_qs = form.objects.all()
        form_ls = [form_i.code for form_i in form_qs]

    context = {"status":{'form': status_ls[0],'date': status_ls[1],'status': status_ls[2],'status_text': status_ls[3],"days":days},
               "receipt_num":receipt_num, "case_range":str(case_range_s)+"-"+str(case_range_e),"form_ls":form_ls,
               "status_qs":status_qs,"page_title":"myCase"}
    return render(request,'mycase/mycase.html',context)

def caseinrange(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the data_type from the client side.
        receipt_num = request.GET.get("recepit_num", None)
        form_type = request.GET.get("form_type", None)
        case_range = request.GET.get("case_range", None)
        selectform = request.GET.get("selectform", None)

        delta_1d = datetime.today().date() + timedelta(days=-2)
        delta_1w = datetime.today().date() + timedelta(days=-8)
        delta_2w = datetime.today().date() + timedelta(days=-15)

        if form_type=="":
            data_dict = {"n_cases": 0, "message":"Form type is not available!"}
            return JsonResponse(data_dict, status=200)

        # check for the data_type.
        if receipt_num != None:
            center = receipt_num[:3]
            year = receipt_num[3:5]
            lb_sc = "LB" if receipt_num[5] == "9" else "SC"
            center_table = center_dict[center.lower() + "_" + lb_sc.lower()]

            if selectform == "yes" and form_type!="":
                case_x =  center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date").first()
                case_x.form=form_type
                case_x.save()


            case_range_base = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)
            case_qs = getcase_in_range(case_range,center,case_range_base,center_table,form_type,receipt_num)

            ##########
            # print(len(case_qs))
            if len(case_qs) > 0:
                status_letter = {"Received":"R", "FP_Taken":"F","Interviewed":"I","RFE":"E","Transferred":"T","Approved":"A","Rejected":"J","Other":"O"}
                status_abbr = {"Received": "REC", "FP_Taken": "FP", "Interviewed": "ITV", "RFE": "RFE", "Transferred": "TRF", "Approved": "APV", "Rejected": "RJC", "Other": "OTH"}

                status_counts = {"Received":0, "FP_Taken":0,"Interviewed":0,"RFE":0,"Transferred":0,"Approved":0,"Rejected":0,"Other":0}
                status_1d = {"Received":0, "FP_Taken":0,"Interviewed":0,"RFE":0,"Transferred":0,"Approved":0,"Rejected":0,"Other":0}
                status_1w = {"Received":0, "FP_Taken":0,"Interviewed":0,"RFE":0,"Transferred":0,"Approved":0,"Rejected":0,"Other":0}
                status_2w = {"Received":0, "FP_Taken":0,"Interviewed":0,"RFE":0,"Transferred":0,"Approved":0,"Rejected":0,"Other":0}

                status_seq = ""
                status_mut = []
                status_dom = []
                i = 0
                used_case = []
                mystatus_l3 = ""
                mypos=-1
                for case_i in case_qs.order_by("receipt_number", "-add_date"):
                    if case_i.receipt_number in used_case: continue
                    else: used_case.append(case_i.receipt_number)

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
                    if case_i.receipt_number==receipt_num:
                        status_mut.append({"ID":case_i.receipt_number,"Num":1.5,"POS":i,"STATUS":status_abbr[l3_name],"ACTDATE":case_i.action_date_x})
                        mystatus_l3 = l3_name
                        mypos = status_counts[l3_name]
                    else:
                        status_mut.append({"ID":case_i.receipt_number,"Num":1,"POS":i,"STATUS":status_abbr[l3_name],"ACTDATE":case_i.action_date_x})
                    status_dom.append({"ID":status_abbr[l3_name],"START":i-0.5,"END":i+0.5})
                n_cases = len(used_case)

                ## merge doamin:
                status_dom_merged = [{"ID":"","START":0,"END":len(case_qs)+1}]
                ID_prev = status_dom[0]["ID"]
                start_i = status_dom[0]["START"]
                for i in range(1,len(status_dom)):
                    if status_dom[i]["ID"] != ID_prev:
                        status_dom_merged.append({"ID":ID_prev,"START":start_i,"END":status_dom[i]["START"]})
                        ID_prev = status_dom[i]["ID"]
                        start_i = status_dom[i]["START"]
                status_dom_merged.append({"ID": ID_prev, "START": start_i, "END": status_dom[i]["END"]})

                for status_i in ["Received","FP_Taken","Interviewed","RFE","Transferred","Approved","Rejected", "Other"]:
                    if status_i == mystatus_l3:
                        break
                    else:
                        mypos += status_counts[status_i]
                pre_apv_poll = n_cases - status_counts["Other"] - status_counts["Rejected"] - status_counts["Approved"]

                if mystatus_l3 in ["Received","FP_Taken","Interviewed","RFE","Transferred"]: mypos_text = "YOU are approaching...("+str(mypos)+"/"+str(pre_apv_poll)+") <i class='fas fa-fighter-jet'></i>"
                elif mystatus_l3 in ["Approved"] :mypos_text = "Congrats! <i class='fas fa-glass-cheers'></i>"
                else:mypos_text = "YOU"

                mypos = round(mypos / n_cases * 100.0)
                ####################
                used_case = []
                recent_apv = {}
                recent_trf = {}
                recent_rfe = {}
                for case_i in case_qs.order_by("-add_date"):  ## here also can use "-action_date_x"
                    ## open the comments, only count the final status of a receipt number(one case can have several status changes within a few days)
                    # if case_i.receipt_number in used_case: continue
                    # else: used_case.append(case_i.receipt_number)

                    l3_name = get_l_status(case_i.status,"L3")
                    if l3_name == "Approved" and len(recent_apv)<5: recent_apv[case_i.receipt_number] = case_i.action_date_x
                    if l3_name == "Transferred" and len(recent_trf)<5: recent_trf[case_i.receipt_number] = case_i.action_date_x
                    if l3_name == "RFE" and len(recent_rfe)<5: recent_rfe[case_i.receipt_number] = case_i.action_date_x
                    if  len(recent_apv)+len(recent_trf) +  len(recent_rfe) >=15: break

                del used_case[:]
                data_dict = {"n_cases":n_cases,"status_counts": list(status_counts.values()),
                             "status_1d":status_1d,"status_1w":status_1w,"status_2w":status_2w,
                             "recent_apv":recent_apv,"recent_trf":recent_trf,"recent_rfe":recent_rfe,
                             "mypos":mypos,"mypos_text":mypos_text,
                             "status_seq": status_seq,"status_mut":status_mut,"status_dom":status_dom_merged}
                return JsonResponse(data_dict, status=200)
            else:   ## queryset is empty
                data_dict = {"n_cases": 0, "message":"Error in reading data!"}
                return JsonResponse(data_dict, status=200)
        else:  ## receipt_num == None
            data_dict = {"n_cases": 0, "message":"Bad request of Recepit/Case number!"}
            return JsonResponse(data_dict, status=200)
    else: ## ajax, GET error
        data_dict = {"n_cases": 0, "message":"Request error!"}
        return JsonResponse(data_dict, status=200)

def nextstatus(request):
    mycase_status = request.GET.get("mystatus", None)
    date_range = request.GET.get("daterange", None)
    form_type = request.GET.get("form_type", None)
    status_level = request.GET.get("status_level", None)
    receipt_num = request.GET.get("recepit_num", None)
    center = request.GET.get("center", None)

    selectform = request.GET.get("selectform", None)

    today = datetime.today()
    if date_range=="past3m":
        date_s = today + timedelta(days=-90)
    elif date_range=="past6m":
        date_s = today + timedelta(days=-180)
    elif date_range=="past9m":
        date_s = today + timedelta(days=-270)
    elif date_range=="past12m":
        date_s = today + timedelta(days=-365)
    else:
        date_s = today + timedelta(days=-365)

    if receipt_num != None or center==None:
        center = receipt_num[:3]
        lb_sc = "LB" if receipt_num[5] == "9" else "SC"
        center_table = center_dict[center.lower() + "_" + lb_sc.lower()]
        if selectform == "yes" and form_type != "":
            case_x = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date").first()
            case_x.form = form_type
            case_x.save()
    else:
        center_table = center_dict[center.lower()]
    case_qs = center_table.objects.filter(form=form_type,action_date_x__gte=date_s).order_by("add_date")
    all_status = {}
    for case_i in case_qs:
        if case_i.receipt_number not in all_status:
            all_status[case_i.receipt_number] = [case_i]
        else:
            all_status[case_i.receipt_number].append(case_i)


    next_status = {}
    to_endstatus = []
    l4_name = get_l_status(mycase_status,"L4")

    if l4_name == "Final":
        next_status["Final"] = [0]
    else:
        for rn_i in all_status:
            rn_i_n = len(all_status[rn_i])
            if rn_i_n <= 1: continue
            rn_i_status_date = ""
            for sn_i in range(rn_i_n):
                status_i = all_status[rn_i][sn_i].status
                if status_level != "L0":
                    status_i_l = get_l_status(status_i, status_level)
                    mycase_status_l = get_l_status(mycase_status,status_level)
                else:
                    status_i_l = status_i
                    mycase_status_l = status_i
                if status_i_l == mycase_status_l and (sn_i+1) < rn_i_n and rn_i_status_date=="":
                    ## rn_i_status_date=="": only save the first pair of status change.
                    rn_i_status_date = all_status[rn_i][sn_i].action_date_x
                    next_s = get_l_status(all_status[rn_i][sn_i+1].status,status_level)
                    next_s_days = (all_status[rn_i][sn_i+1].action_date_x - all_status[rn_i][sn_i].action_date_x).days
                    if next_s_days <= 0: continue
                    if next_s not in next_status:
                        next_status[next_s] = [next_s_days]
                    else:
                        next_status[next_s].append(next_s_days)
                if rn_i_status_date !="" and get_l_status(status_i, "L4") == "Final":
                    tofinal_days = (all_status[rn_i][sn_i].action_date_x-rn_i_status_date).days
                    if tofinal_days > 0:
                        to_endstatus.append(tofinal_days)
                    break

    for status_i in next_status:
        x_len = len(next_status[status_i])
        x_avg = int(sum(next_status[status_i])/x_len)
        x_mid = median(next_status[status_i])
        x_min = min(next_status[status_i])
        x_max = max(next_status[status_i])

        next_status[status_i] = [x_len,x_avg,x_mid,x_min,x_max]
    to_endstatus = [int(sum(to_endstatus)/len(to_endstatus)),median(to_endstatus),min(to_endstatus),max(to_endstatus)]
    # print(next_status,to_endstatus)
    data_dict ={"next_status":next_status, "to_endstatus":to_endstatus}
    return JsonResponse(data_dict, status=200)


def visabulletin(request):
    if request.method == "GET":
        return render(request,'mycase/visabulletin.html')
    elif request.method == "POST":
        return render(request,'mycase/visabulletin.html')

def dailyrecords(request):
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("formselect", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("formselect", None)

    if selectform == None or center == None:
        data_dict = {"label_ls":[], "count_ls":[]}
        return JsonResponse(data_dict, status=200)

    date_s = datetime.today() + timedelta(days=-365)
    count_qs = status_daily.objects.filter(form=selectform,center=center,add_date__gte= date_s).order_by("add_date")
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
        date_ls.append(count_i.add_date.date()+ timedelta(days=-1))
        rec.append(count_i.new_n)
        fp.append(count_i.fp_taken_n + count_i.fp_schduled_n)
        itv.append(count_i.iv_schduled_n + count_i.iv_done_n)
        rfe.append(count_i.rfe_sent_n + count_i.rfe_received_n)
        trf.append(count_i.transferred_n)
        apv.append(count_i.approved_n+count_i.mailed_n + count_i.produced_n)
        rej.append(count_i.rejected_n+count_i.terminated_n)
        pending.append(count_i.pending_n)
        oth.append(count_i.others_n  + count_i.notice_sent_n + count_i.hold_n+count_i.return_hold_n + count_i.withdrawal_acknowledged_n)

    count_ls = [rec,fp,itv, rfe, trf, apv, rej, oth,pending]
    data_dict = {"label_ls": date_ls,"count_ls":count_ls}
    return JsonResponse(data_dict, status=200)

def dashbord(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

    context = {"page_title": "Dashbord", "form_ls": form_ls}
    return render(request, 'mycase/dashbord.html', context)

def rnrangecount(request):
    if request.method == "GET":
        center = request.GET.get("center", None)
        selectform = request.GET.get("formselect", None)
        fy = request.GET.get("fy", None)
        statuslevel = request.GET.get("statuslevel", None)
    elif request.method == "POST":
        center = request.POST.get("center", None)
        selectform = request.POST.get("formselect", None)
        fy = request.POST.get("fy", None)
        statuslevel = request.POST.get("statuslevel", None)

    if selectform == None or center == None or fy==None:
        data_dict = {"dataset":0}
        return JsonResponse(data_dict, status=200)

    center_table = center_dict[center.lower()]
    fy = fy[-2:]
    c_code = center.split("_")[0]
    lsi = center.split("_")[1]
    rn_range = 5000

    if statuslevel == "L3":
        color = color8
        dataset_labels = ['Received', 'FP_Taken', 'Interviewed', 'RFE', 'Transferred', 'Approved', 'Rejected', 'Other']
    if statuslevel == "L2":
        color = color20
        dataset_labels = ['Received', 'FP_Scheduled', 'FP_Taken', 'InterviewScheduled', 'InterviewCompleted',
                          'RFE_Sent', 'RFE_Received', 'Transferred', 'Approved', 'Produced', 'Mailed', 'Pending',
                          'Hold', 'ReturnHold', 'NoticeSent', 'Reopened', 'Other', 'Rejected', 'Terminated',
                          'WithdrawalAcknowledged']
    rn_pattern = c_code+fy
    case_qs = center_table.objects.filter(form=selectform,receipt_number__startswith=rn_pattern).order_by("receipt_number","-add_date")

    print("1",datetime.now())
    status_count = {}
    rn_status = {}
    for case_i in case_qs:
        if case_i.receipt_number in rn_status: continue
        status_l = get_l_status(case_i.status, statuslevel)
        rn_status[case_i.receipt_number] = 1

        rn = int(case_i.receipt_number[3:])
        range_key = rn - (rn % rn_range)
        range_key = c_code + str(range_key) + "-" + str(range_key + rn_range - 1)[-4:]

        if range_key not in status_count:
            if statuslevel=="L2":
                status_count[range_key] = {
                'Received':0,'FP_Scheduled':0,'FP_Taken':0,'InterviewScheduled':0,'InterviewCompleted':0,
                'RFE_Sent':0,'RFE_Received':0,'Transferred':0,'Approved':0,'Produced':0,'Mailed':0,'Pending':0,
                'Hold':0,'ReturnHold':0,'NoticeSent':0,'Reopened':0,'Other':0,'Rejected':0,'Terminated':0,'WithdrawalAcknowledged':0
                }

            if statuslevel=="L3":
                status_count[range_key] = {
                    'Received':0,'FP_Taken':0,'Interviewed':0,'RFE':0,'Transferred':0,'Approved':0,'Rejected':0, 'Other':0
                }
        status_count[range_key][status_l] += 1

    labels = list(status_count.keys())
    dataset = {}
    for dataset_i in dataset_labels:
        dataset[dataset_i] = []
        for rnrange_i in status_count:
            dataset[dataset_i].append(status_count[rnrange_i][dataset_i])

    data_dict = {"dataset":dataset,"label":labels,"color":color}
    return JsonResponse(data_dict, status=200)

def process(request):
    form_qs = form.objects.all()
    form_ls = [form_i.code for form_i in form_qs]

    context = {"page_title": "Case range process", "form_ls": form_ls}
    return render(request, 'mycase/process.html', context)


def today(request):
    if request.method == "GET":
        return render(request,'mycase/today.html')
    elif request.method == "POST":
        return render(request,'mycase/today.html')


def about(request):
    if request.method == "GET":
        return render(request,'mycase/about.html')
    elif request.method == "POST":
        return render(request,'mycase/about.html')

