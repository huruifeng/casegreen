import csv
import json
import os

from django.contrib.auth import authenticate, login
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from ctrlpanel.functions.utils import bkpTable, run_initalization, run_center
from mycase.models import *

# Create your views here.
@login_required()
def index(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

    sys_params,created = sysparam.objects.get_or_create(pk=1,defaults={
        "centers": "LIN,MSC,SRC,EAC,WAC,YSC",
        "fiscal_year_n": 3,
        "crawler_time": "21:05:00",
        "crawler_number": 1,
        "sys_status": "Running"
    })
    context = {'sys_params': sys_params}
    return render(request,'ctrlpanel/index.html',context)

@login_required()
# @user_passes_test(lambda u: u.is_superuser)
def ctrl_dashbord(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

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
                    return redirect("mycase:home")
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    return HttpResponse(state)

def exportDB(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

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
        return HttpResponse("ERROR: Please Login!")

    if request.is_ajax and request.method == "POST":
        # try:
        # backup data
        case_status_tables = [case_status_lin_lb, case_status_msc_lb, case_status_src_lb, case_status_wac_lb,
                              case_status_eac_lb, case_status_ysc_lb,
                              case_status_lin_sc, case_status_msc_sc, case_status_src_sc, case_status_wac_sc,
                              case_status_eac_sc, case_status_ysc_sc,
                              case_status_ioe]
        model_ls = [sysparam, status, status_daily, form, center_running] + case_status_tables
        for m_i in model_ls:
            data = bkpTable(request, m_i.objects.all())

        # Init
        run_initalization(request)
        return HttpResponse("OK")
        # except Exception as e:
        #     return HttpResponse(e)

def sysupdate(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

    if request.is_ajax and request.method == "POST":
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
        return HttpResponse("ERROR: Please Login!")

    if request.is_ajax and request.method == "POST":
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

        ## delete the static files
        file_ls = os.listdir("mycase/data/statistics/center_range_count")
        for f_i in file_ls:
            while True:
                try:
                    os.remove("mycase/data/statistics/center_range_count/"+f_i)
                    break
                except OSError:
                    pass

        print("*******************************")
        print("All done!")
        print("*******************************")
        return HttpResponse("OK")

def centerstatus(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

    qs_json = {}
    if request.is_ajax and request.method == "POST":
        center_status = center_running.objects.all()
        qs_json = serializers.serialize('json', center_status)

    return HttpResponse(qs_json, content_type='application/json')


def visabulletin(request):
    if (not request.user.is_authenticated) or (not request.user.is_superuser):
        return HttpResponse("ERROR: Please Login!")

    if request.method == "GET":
        return render(request,'ctrlpanel/visabulletin.html')
    elif request.method == "POST":
        return render(request,'ctrlpanel/visabulletin.html')






