from django.contrib import admin

# Register your models here.

from .models import *


class sysparamAdmin(admin.ModelAdmin):
    list_display = ["centers", "fiscal_year_n", "crawler_time", "crawler_number","sys_status"]
admin.site.register(sysparam, sysparamAdmin)


class statusAdmin(admin.ModelAdmin):
    list_display = ["name", "l1", "l2", "l3","l4", "note", "add_date"]
admin.site.register(status, statusAdmin)


class formAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "description"]
admin.site.register(form, formAdmin)

class status_dailyAdmin(admin.ModelAdmin):
    list_display = ["received_n", "rfe_sent_n", "approved_n","fp_schduled_n", "fp_taken_n", "iv_schduled_n",
                    "iv_done_n", "pending_n", "rejected_n", "terminated_n","transferred_n", "others_n", "add_date","date_number"]
admin.site.register(status_daily,status_dailyAdmin)


class center_runningAdmin(admin.ModelAdmin):
    list_display = ["center_lsi", "status", "start","end"]
admin.site.register(center_running,center_runningAdmin)

class visabulletinAdmin(admin.ModelAdmin):
    list_display = ["category", "conutry", "formonth","tableA","tableB", "visadate","adddate"]
admin.site.register(visabulletin,visabulletinAdmin)

class statustransAdmin(admin.ModelAdmin):
    list_display = ["action_date", "source_status", "dest_status","count","center", "form_type"]
admin.site.register(status_trans,statustransAdmin)

#######################
## LB
class case_status_lin_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_lin_lb, case_status_lin_lbAdmin)

class case_status_msc_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_msc_lb, case_status_msc_lbAdmin)

class case_status_src_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_src_lb, case_status_src_lbAdmin)

class case_status_wac_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_wac_lb, case_status_wac_lbAdmin)

class case_status_eac_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_eac_lb, case_status_eac_lbAdmin)

class case_status_ysc_lbAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_ysc_lb, case_status_ysc_lbAdmin)

## SC
class case_status_lin_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_lin_sc, case_status_lin_scAdmin)

class case_status_msc_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_msc_sc, case_status_msc_scAdmin)

class case_status_src_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_src_sc, case_status_src_scAdmin)

class case_status_wac_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_wac_sc, case_status_wac_scAdmin)

class case_status_eac_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_eac_sc, case_status_eac_scAdmin)

class case_status_ysc_scAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_ysc_sc, case_status_ysc_scAdmin)

class case_status_ioeAdmin(admin.ModelAdmin):
    list_display = ["receipt_number", "form", "status", "action_date", "add_date", "date_number"]
admin.site.register(case_status_ioe, case_status_ioeAdmin)


