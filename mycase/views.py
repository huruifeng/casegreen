import json
from datetime import datetime, timedelta

from django.db.models import Max, F
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from ctrlpanel.functions.utils import get_status_dict
from mycase.functions.utils import get_status
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
    status_ls = get_status(receipt_num)

    ## read data from database
    center_table = center_dict[center.lower()+"_"+ lb_sc.lower()]
    status_qs = center_table.objects.filter(receipt_number=receipt_num)
    if status_qs.exists():
        status_qs = status_qs.order_by("add_date")
        if len(status_ls) >= 3:
            time_x = datetime.strptime(status_ls[1], "%B %d, %Y")
            days = (datetime.now() - time_x).days
            if status_ls[0]=="":
                status_ls[0] = status_qs.last().form
            if status_qs.last().status != status_ls[2]:
                status_dict = get_status_dict()
                case_stage = "Processing"
                if status_ls[2] in status_dict:
                    l3_name = status_dict[status_ls[2]]["L3"]
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
            status_ls = [status_qs.last().form,status_qs.last().action_date, status_qs.last().status, ""]
            time_x = datetime.strptime(status_qs.last().action_date, "%B %d, %Y")
            days = (datetime.now()-time_x).days
    else:
        if len(status_ls) < 3:
            status_ls = ["NA","NA", "Cannot get the data!", ""]
            days = "NA"
        else:
            time_x = datetime.strptime(status_ls[1], "%B %d, %Y")
            days = (datetime.now() - time_x).days
            status_dict = get_status_dict()
            case_stage = "Processing"
            if status_ls[2] in status_dict:
                l3_name = status_dict[status_ls[2]]["L3"]
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

    case_range_s = int(receipt_num[3:]) - int(int(receipt_num[3:])%5000)
    case_range_e = case_range_s + 4999

    form_ls = []
    if status_ls[0] == "":
        ## form type is not available
        form_qs = form.objects.all()
        form_ls = [form_i.code for form_i in form_qs]

    context = {"status":{'form': status_ls[0],'date': status_ls[1],'status': status_ls[2],'status_text': status_ls[3],"days":days},
               "receipt_num":receipt_num, "case_range":str(case_range_s)+"-"+str(case_range_e),"form_ls":form_ls,
               "status_qs":status_qs}
    return render(request,'mycase/mycase.html',context)

def visabulletin(request):
    if request.method == "GET":
        return render(request,'mycase/visabulletin.html')
    elif request.method == "POST":
        return render(request,'mycase/visabulletin.html')

def caseinrange(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the data_type from the client side.
        receipt_num = request.GET.get("recepit_num", None)
        form_type = request.GET.get("form_type", None)
        case_range = request.GET.get("case_range", None)

        if form_type=="":
            return JsonResponse({}, status=400)

        # check for the data_type.
        if receipt_num != None:
            center = receipt_num[:3]
            year = receipt_num[3:5]
            lb_sc = "LB" if receipt_num[5] == "9" else "SC"
            center_table = center_dict[center.lower() + "_" + lb_sc.lower()]

            case_range_base = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)

            if case_range=="rn_range":
                case_range_s = center + str(case_range_base)
                case_range_e = center + str(case_range_base + 4999)
                case_qs = center_table.objects.filter(form=form_type,receipt_number__range=(case_range_s, case_range_e)).order_by("receipt_number","-add_date")
            elif case_range == "rn_n200":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:201]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_n500":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:501]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_n1000":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("-receipt_number")[:1001]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_p200":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:201]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_p500":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:501]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_p1000":
                case_range_s = receipt_num
                case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs = [x["receipt_number"] for x in case_qs.order_by("receipt_number")[:1001]]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
            elif case_range == "rn_np200":
                case_range_s = receipt_num
                case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
                case_qs1 = case_qs1.order_by("-receipt_number")[:200]
                case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs2 = case_qs2.order_by("receipt_number")[:201]
                case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
                del case_qs1
                del case_qs2
            elif case_range == "rn_np500":
                case_range_s = receipt_num
                case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
                case_qs1 = case_qs1.order_by("-receipt_number")[:500]
                case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs2 = case_qs2.order_by("receipt_number")[:501]
                case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
                del case_qs1
                del case_qs2
            elif case_range == "rn_np1000":
                case_range_s = receipt_num
                case_qs1 = center_table.objects.filter(form=form_type, receipt_number__lt=case_range_s).values("receipt_number").distinct()
                case_qs1 = case_qs1.order_by("-receipt_number")[:1000]
                case_qs2 = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).values("receipt_number").distinct()
                case_qs2 = case_qs2.order_by("receipt_number")[:1001]
                case_qs = [x["receipt_number"] for x in case_qs1] + [x["receipt_number"] for x in case_qs2]
                case_qs = center_table.objects.filter(form=form_type, receipt_number__in=case_qs).order_by("receipt_number", "-add_date")
                del case_qs1
                del case_qs2
            elif case_range == "rd_n1m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-30)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd.rd_date)).order_by("receipt_number","-add_date")
            elif case_range == "rd_n2m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-60)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd.rd_date)).order_by("receipt_number","-add_date")
            elif case_range == "rd_n3m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-90)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd.rd_date)).order_by("receipt_number","-add_date")
            elif case_range == "rd_p1m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_e = case_rd.rd_date + timedelta(days=+30)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rd_p2m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_e = case_rd.rd_date + timedelta(days=+60)
                case_qs = center_table.objects.filter(form=form_type,rd_date__range=(case_rd.rd_date,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rd_p3m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_e = case_rd.rd_date + timedelta(days=+90)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd.rd_date,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rd_np1m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-30)
                case_rd_e = case_rd.rd_date + timedelta(days=+30)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rd_np2m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-60)
                case_rd_e = case_rd.rd_date + timedelta(days=+60)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rd_np3m":
                case_rd = center_table.objects.filter(receipt_number=receipt_num).order_by("-add_date")[0]
                case_rd_s = case_rd.rd_date + timedelta(days=-90)
                case_rd_e = case_rd.rd_date + timedelta(days=+90)
                case_qs = center_table.objects.filter(form=form_type, rd_date__range=(case_rd_s,case_rd_e)).order_by("receipt_number","-add_date")
            elif case_range == "rn_fy":
                center_year = center + year
                case_qs = center_table.objects.filter(form=form_type, receipt_number__startswith=center_year).order_by("receipt_number","-add_date")
            else:
                case_range_s = center + str(case_range_base)
                case_range_e = center + str(case_range_base + 4999)
                case_qs = center_table.objects.filter(form=form_type, receipt_number__range=(case_range_s, case_range_e)).order_by("receipt_number","-add_date")

            # print(len(case_qs))
            if len(case_qs) > 0:
                status_letter = {"Received":"R", "FP_Taken":"F","Interviewed":"I","RFE":"E","Transferred":"T","Approved":"A","Rejected":"J","Other":"O"}
                status_abbr = {"Received": "REC", "FP_Taken": "FP", "Interviewed": "ITV", "RFE": "RFE", "Transferred": "TRF", "Approved": "APV", "Rejected": "RJC", "Other": "OTH"}
                status_dict = get_status_dict()

                status_counts = {"Received":0, "FP_Taken":0,"Interviewed":0,"RFE":0,"Transferred":0,"Approved":0,"Rejected":0,"Other":0}
                status_seq = ""
                status_mut = []
                status_dom = []
                i = 0

                used_case = []
                for case_i in case_qs:
                    if case_i.receipt_number in used_case:
                        continue
                    else:
                        used_case.append(case_i.receipt_number)

                    ####
                    i += 1
                    if case_i.status in status_dict:
                        l3_name = status_dict[case_i.status]["L3"]
                    else:
                        l3_name = "Other"
                    status_counts[l3_name] += 1
                    status_seq += status_letter[l3_name]
                    if case_i.receipt_number==receipt_num:
                        status_mut.append({"ID":case_i.receipt_number,"Num":1.5,"POS":i,"STATUS":status_abbr[l3_name],"ACTDATE":case_i.action_date})
                    else:
                        status_mut.append({"ID":case_i.receipt_number,"Num":1,"POS":i,"STATUS":status_abbr[l3_name],"ACTDATE":case_i.action_date})
                    status_dom.append({"ID":status_abbr[l3_name],"START":i-0.5,"END":i+0.5})
                n_cases = len(used_case)
                del used_case[:]

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

                data_dict = {"n_cases":n_cases,"status_counts": list(status_counts.values()),"status_seq": status_seq,"status_mut":status_mut,"status_dom":status_dom_merged}
                return JsonResponse(data_dict, status=200)
            else:
                ## queryset is empty
                data_dict = {"n_cases": 0, "status_counts": 0,"status_seq": "", "status_mut": [], "status_dom": []}
                return JsonResponse(data_dict, status=200)
        else:  ## receipt_num == None
            data_dict = {"n_cases": 0, "status_counts": 0, "status_seq": "", "status_mut": [], "status_dom": []}
            return JsonResponse(data_dict, status=200)
    else: ## ajax, GET
        data_dict = {"n_cases": 0, "status_counts": 0, "status_seq": "", "status_mut": [], "status_dom": []}
        return JsonResponse(data_dict, status=200)

