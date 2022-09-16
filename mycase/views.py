import json
from datetime import datetime

from django.db.models import Q
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
    context = {"status":{'form': status_ls[0],'date': status_ls[1],'status': status_ls[2],'status_text': status_ls[3],"days":days},
               "receipt_num":receipt_num, "case_range":str(case_range_s)+"-"+str(case_range_e),
               "status_qs":status_qs}
    return render(request,'mycase/mycase.html',context)

def visabulletin(request):
    if request.method == "GET":
        return render(request,'mycase/visabulletin.html')
    elif request.method == "POST":
        return render(request,'mycase/visabulletin.html')

def getjson(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the data_type from the client side.
        data_type = request.GET.get("data_type", None)
        # check for the data_type.
        if data_type=="lollipop":
            data_dict = {}
            with open("mycase/data/O14976_mutation.txt","r") as f:
                mut_str = f.read()
            with open("mycase/data/O14976_domain.txt","r") as f:
                domain_str = f.read()
            data_dict['mut_sites'] = mut_str
            data_dict['domains'] = domain_str
            return HttpResponse(json.dumps(data_dict), status=200)
        else:
            return JsonResponse({}, status=400)

    return JsonResponse({}, status=400)

def caseinrange(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the data_type from the client side.
        receipt_num = request.GET.get("recepit_num", None)
        form_type = request.GET.get("form_type", None)
        case_range = request.GET.get("form_type", None)

        if form_type=="":
            return JsonResponse({}, status=400)

        # check for the data_type.
        if receipt_num != None:
            center = receipt_num[:3]
            year = receipt_num[3:5]
            lb_sc = "LB" if receipt_num[5] == "9" else "SC"
            center_table = center_dict[center.lower() + "_" + lb_sc.lower()]

            case_range_s = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)

            if case_range=="rn_range":
                case_range_s = center + str(case_range_s)
                case_range_e = center + str(case_range_s + 4999)
                case_qs = center_table.objects.filter(form=form_type,receipt_number__range=(case_range_s, case_range_e))
            elif case_range == "rn_n200":
                case_range_s = center + str(case_range_s)
                case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).order_by("-receipt_num")[:201]
            elif case_range == "rn_n500":
                case_range_s = center + str(case_range_s)
                case_qs = center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).order_by("-receipt_num")[:501]
            elif case_range == "rn_p200":
                case_range_s = center + str(case_range_s)
                case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).order_by("receipt_num")[:201]
            elif case_range == "rn_p500":
                case_range_s = center + str(case_range_s)
                case_qs = center_table.objects.filter(form=form_type, receipt_number__gte=case_range_s).order_by("receipt_num")[:501]
            elif case_range == "rn_np200":
                case_range_s = center + str(case_range_s)
                case_qs = (center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).order_by("receipt_num")[:201]) | \
                          (center_table.objects.filter(form=form_type, receipt_number__gt=case_range_s).order_by("receipt_num")[:200])
            elif case_range == "rn_np500":
                case_range_s = center + str(case_range_s)
                case_qs = (center_table.objects.filter(form=form_type, receipt_number__lte=case_range_s).order_by("receipt_num")[:501]) | \
                          (center_table.objects.filter(form=form_type, receipt_number__gt=case_range_s).order_by("receipt_num")[:500])
            elif case_range == "rn_n1m":
                pass
            elif case_range == "rn_n2m":
                pass
            elif case_range == "rn_n3m":
                pass
            elif case_range == "rn_p1m":
                pass
            elif case_range == "rn_p2m":
                pass
            elif case_range == "rn_p3m":
                pass
            elif case_range == "rn_np1m":
                pass
            elif case_range == "rn_np2m":
                pass
            elif case_range == "rn_np3m":
                pass
            elif case_range == "rn_fy":
                pass
            else:
                pass







            case_range_s = int(receipt_num[3:]) - int(int(receipt_num[3:]) % 5000)
            case_range_e = case_range_s + 4999
            return HttpResponse(json.dumps(data_dict), status=200)
        else:
            return JsonResponse({}, status=400)
    else:
        return JsonResponse({}, status=400)

