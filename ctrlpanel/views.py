import csv
from datetime import datetime,timedelta
import json
import os

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from ctrlpanel.functions.utils import bkp_table, run_initalization, run_center
from mycase.functions.utils import generate_overview
from mycase.models import *

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


# Create your views here.
@login_required()
def index(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    sys_params,created = sysparam.objects.get_or_create(pk=1,defaults={
        "centers": "LIN,MSC,SRC,EAC,WAC,YSC",
        "fiscal_year_n": 3,
        "crawler_time": "21:05",
        "crawler_number": 1,
        "sys_status": "Running"
    })
    sys_params.crawler_time = sys_params.crawler_time.strftime("%H:%M")
    context = {'sys_params': sys_params}
    return render(request,'ctrlpanel/index.html',context)

@login_required()
# @user_passes_test(lambda u: u.is_superuser)
def ctrl_dashbord(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    return render(request,'ctrlpanel/dashbord.html')


def login_view(request):
    username = password = ''
    next_url=""
    if request.GET:
        next_url = request.GET.get("next")

    if request.POST:
        username = request.POST['username']
        password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # print(next_url)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("ctrlpanel:ctrlhome")
            else:
                state = "Your account is not active, please contact the site admin."
                return HttpResponse(state)
        else:
            state = "Your username and/or password were incorrect."
            return HttpResponse(state)
    else:
        return redirect("login")



def exportDB(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportDB.csv"'
    # the csv writer
    writer = csv.writer(response, delimiter=",")

    case_status_tables = [case_status_lin_lb, case_status_msc_lb, case_status_src_lb, case_status_wac_lb,
                          case_status_eac_lb, case_status_ysc_lb,
                          case_status_lin_sc, case_status_msc_sc, case_status_src_sc, case_status_wac_sc,
                          case_status_eac_sc, case_status_ysc_sc,
                          case_status_ioe]
    model_ls = [sysparam, status, status_daily,form,center_running] + case_status_tables
    for m_i in model_ls:

        queryset = m_i.objects.all()
        model = queryset.model
        table_name = model._meta.db_table
        model_fields = model._meta.fields + model._meta.many_to_many
        field_names = [field.name for field in model_fields]
        # Write a first row for the Table name
        writer.writerow(["##"+table_name])
        # Write a row with header information
        writer.writerow(field_names)
        # Write data rows
        for row in queryset:
            values = []
            for field in field_names:
                value = getattr(row, field)
                if callable(value):
                    try:
                        value = value() or ''
                    except:
                        value = 'Error retrieving value'
                if value is None:
                    value = ''
                values.append(value)
            writer.writerow(values)
    return response

def sysinit(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    if request.method == "POST":
        # try:
        # backup data
        case_status_tables = [case_status_lin_lb, case_status_msc_lb, case_status_src_lb, case_status_wac_lb,
                              case_status_eac_lb, case_status_ysc_lb,
                              case_status_lin_sc, case_status_msc_sc, case_status_src_sc, case_status_wac_sc,
                              case_status_eac_sc, case_status_ysc_sc,
                              case_status_ioe]
        model_ls = [sysparam, status, status_daily, form, center_running] + case_status_tables
        for m_i in model_ls:
            data = bkp_table(request, m_i.objects.all())

        # Init
        run_initalization(request)
        return HttpResponse("OK")
        # except Exception as e:
        #     return HttpResponse(e)

def sysupdate(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    if request.method == "POST":
        # get the data from the client side.
        centers = request.POST.get("centers", None)
        fys_n = request.POST.get("fys", None)
        crawler_t = request.POST.get("crawler_t", None)+":00"
        crawler_n = request.POST.get("crawler_n", None)

        sys_params,created = sysparam.objects.update_or_create(pk=1,defaults={
            "centers":centers,
            "fiscal_year_n": fys_n,
            "crawler_time":crawler_t,
            "crawler_number": crawler_n
        })

        return HttpResponse("OK")

def centerrun(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    ## delete the static files
    file_ls = os.listdir("mycase/data/statistics/center_range_count")
    for f_i in file_ls:
        while True:
            try:
                os.remove("mycase/data/statistics/center_range_count/" + f_i)
                break
            except OSError:
                pass
    ##
    file_ls = os.listdir("mycase/data/statistics/center_range_count_heatmap")
    for f_i in file_ls:
        while True:
            try:
                os.remove("mycase/data/statistics/center_range_count_heatmap/" + f_i)
                break
            except OSError:
                pass
    ##
    file_ls = os.listdir("mycase/data/statistics/center_rd_count")
    for f_i in file_ls:
        while True:
            try:
                os.remove("mycase/data/statistics/center_rd_count/" + f_i)
                break
            except OSError:
                pass

    if request.method == "POST":
        # get the data from the client side.
        centers = request.POST.get("centers", None)
        center_ls = centers.split(",")
        for center_i in center_ls:
            try:
                center_running.objects.filter(center_lsi=center_i.upper()).update(status="Pend")
            except Exception as e:
                pass

        for center_i in center_ls:
            return_code = run_center(request,center_i)
            if "skip" in return_code.lower():
                continue

            if "error" in return_code.lower():
                return HttpResponse(return_code)

        ####
        print("-------------------------------")
        print("Generate overview...")
        generate_overview(center_ls)
        print(centers)
        print("Generate overview... Done!")

        print("*******************************")
        print("All done!")
        print("*******************************")
        return HttpResponse("OK")

def centerstatus(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    qs_json = {}
    if request.method == "POST":
        center_status = center_running.objects.all()
        qs_json = serializers.serialize('json', center_status)

    return HttpResponse(qs_json, content_type='application/json')


def checkcase(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    if request.method == "GET":
        return render(request,'ctrlpanel/ctrlcheckcase.html')
    elif request.method == "POST":
        return render(request,'ctrlpanel/ctrlcheckcase.html')


def checkcase_query(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return redirect("ctrlpanel:ctrllogin")
        # return HttpResponse("Login: Please Login!")

    rn = ""
    if request.method == "POST":
        rn = request.POST.get("rn",None)

    if request.method == "GET":
        rn = request.GET.get("rn",None)

    if rn == None or rn=="":
        return JsonResponse({"data":"Error: Receipt is None!"})

    center = rn[:3].lower()
    if center not in ["msc","lin","src","wac","eac","ysc","ioe"]:
        return JsonResponse({"data": "Error: Center is None!"})

    ls = ""
    if center!="ioe":
        ls = "lb" if rn[5]=="9" else "sc"
    center_table = center_dict[center+ "_" + ls]

    case_qs = center_table.objects.filter(receipt_number=rn.upper()).order_by("add_date")
    # print(list(case_qs.values()))
    if len(case_qs)>0:
        return JsonResponse({"data": list(case_qs.values())},safe=False, status=200)
    else:
        return JsonResponse({"data": "Error:No record in the database!"})
def checkcase_update(request):
    rd_date_show = request.POST.get("rd_date_show", None)
    rd_date_show = datetime.strptime(rd_date_show, "%Y-%m-%d")

    form_type_show = request.POST.get("form_type_show", None)
    receipt_number_show = request.POST.get("receipt_number_show", None)

    # action_date = request.POST.getlist("action_date", None)
    status = request.POST.getlist("status", None)
    case_stage = request.POST.getlist("case_stage", None)
    action_date_x = request.POST.getlist("action_date_x", None)
    add_date = request.POST.getlist("add_date", None)
    # date_number = request.POST.getlist("date_number", None)

    if receipt_number_show == None or receipt_number_show=="":
        return JsonResponse({"data":"Error: Receipt is None!"})

    center = receipt_number_show[:3].lower()
    if center not in ["msc","lin","src","wac","eac","ysc","ioe"]:
        return JsonResponse({"data": "Error: Center is None!"})

    ls = ""
    if center!="ioe":
        ls = "lb" if receipt_number_show[5]=="9" else "sc"
    center_table = center_dict[center+ "_" + ls]

    try:
        for i in range(len(action_date_x)):
            action_date_x_i = datetime.strptime(action_date_x[i], "%Y-%m-%d")
            action_date_i = action_date_x_i.strftime("%B %d, %Y")

            if len(add_date[i]) < 15:
                add_date[i] = add_date[i]+"T06:01:01.001"
            add_date_i = datetime.strptime(add_date[i], "%Y-%m-%dT%H:%M:%S.%f")
            date_number_i =  (add_date_i - datetime(2000, 1, 1)).days

            center_table.objects.update_or_create(receipt_number=receipt_number_show, form=form_type_show,status=status[i],action_date_x=action_date_x_i,
                                                  defaults={
                                                      "action_date":action_date_i,
                                                      "case_stage": case_stage[i],
                                                      "rd_date" : rd_date_show,
                                                      "add_date": add_date_i,
                                                      "date_number" : date_number_i
                                                  })
        return JsonResponse({"data": "Update - OK!"})
    except Exception as e:
        return JsonResponse({"data": "Error -"+str(e)})

def checkcase_del(request):
    status = request.POST.get("status", None)
    form = request.POST.get("form", None)
    action_date_x =request.POST.get("action_date_x", None)
    date_number = request.POST.get("date_number", None)
    rn =request.POST.get("rn", None)

    if rn == None or rn == "":
        return JsonResponse({"data": "Error: Receipt is None!"})

    center = rn[:3].lower()
    if center not in ["msc", "lin", "src", "wac", "eac", "ysc", "ioe"]:
        return JsonResponse({"data": "Error: Center is None!"})

    ls = ""
    if center != "ioe":
        ls = "lb" if rn[5] == "9" else "sc"
    center_table = center_dict[center + "_" + ls]

    ## Delete record
    try:
        center_table.objects.filter(receipt_number=rn, status=status,action_date_x=action_date_x,date_number=date_number,form=form).delete()
        return JsonResponse({"data": "Delete - OK!"})
    except Exception as e:
        return JsonResponse({"data": "Error -"+str(e)})







