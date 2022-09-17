from django.db import models
from datetime import date, datetime


# Create your models here.
class sysparam(models.Model):
    centers = models.CharField(max_length=64)
    fiscal_year_n = models.IntegerField()
    crawler_time = models.TimeField()
    crawler_number = models.IntegerField()
    sys_status = models.CharField(max_length=16)

    def centers_as_list(self):
        return [x.strip().lower() for x in self.centers.split(',')]

    def __str__(self):
        return f"Centers: {self.centers}\n" \
               f"Num of fiscal years: {self.fiscal_year_n}\n" \
               f"Run crawler at: {self.crawler_time}\n" \
               f"Num of crawler: {self.crawler_number}\n" \
               f"System: {self.crawler_number}\n"


class center_running(models.Model):
    ## running or not
    center_choices = [
        ('LIN_LB', 'LIN_LB'),
        ('MSC_LB', 'MSC_LB'),
        ('SRC_LB', 'SRC_LB'),
        ('WAC_LB', 'WAC_LB'),
        ('EAC_LB', 'EAC_LB'),
        ('YSC_LB', 'YSC_LB'),
        ('LIN_SC', 'LIN_SC'),
        ('MSC_SC', 'MSC_SC'),
        ('SRC_SC', 'SRC_SC'),
        ('WAC_SC', 'WAC_SC'),
        ('EAC_SC', 'EAC_SC'),
        ('YSC_SC', 'YSC_SC'),
        ('IOE', 'IOE'),
    ]
    center_lsi = models.CharField(max_length=32,choices=center_choices, default="" )
    status = models.CharField(max_length=16)
    start = models.DateTimeField()
    end = models.DateTimeField()
    update_day = models.IntegerField()

    def __str__(self):
        return f"{self.center_lsi}-Start:{self.start},End:{self.end}\n"


class status(models.Model):
    name = models.CharField(max_length=128)
    ## high level means more general, low level means more detailed information
    l1 = models.CharField(max_length=64)
    l2 = models.CharField(max_length=32)
    l3 = models.CharField(max_length=16)
    l4 = models.CharField(max_length=16)
    note = models.CharField(max_length=256)
    add_date = models.DateTimeField('date added')

    def __str__(self):
        return f"{self.name}:{self.l1},{self.l2},{self.l3},{self.l4}\n"


class form(models.Model):
    code = models.CharField(max_length=8, default="")
    name = models.CharField(max_length=128)
    description = models.TextField()
    add_date = models.DateTimeField('date added',auto_now=True, blank=True)

    def __str__(self):
        return "{}:{}\n".format(self.code, self.name)

class status_daily(models.Model):
    center = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    new_n = models.IntegerField(default=0)
    received_n = models.IntegerField()
    rfe_sent_n = models.IntegerField()
    rfe_received_n = models.IntegerField()
    approved_n = models.IntegerField()
    fp_schduled_n = models.IntegerField()
    fp_taken_n = models.IntegerField()
    iv_schduled_n = models.IntegerField()
    iv_done_n = models.IntegerField()
    rejected_n = models.IntegerField()
    terminated_n = models.IntegerField()
    transferred_n = models.IntegerField()
    hold_n = models.IntegerField()
    notice_sent_n = models.IntegerField()
    pending_n = models.IntegerField()
    mailed_n = models.IntegerField()
    produced_n = models.IntegerField()
    return_hold_n = models.IntegerField()
    withdrawal_acknowledged_n = models.IntegerField()
    others_n = models.IntegerField()
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    def __str__(self):
        return f"Table to record the daily processings in center:{self.center}!\n"

class visabulletin(models.Model):
    country_choices = [
        ('CHINA', 'China'),
        ('INDIA', 'India'),
        ('MEXICO', 'Mexico'),
        ('PHILIPPINES', 'Philippines'),
        ('EGH', 'El Salvador/Guatemala/Honduras'),
        ('OTHERS', 'Others'),
    ]
    tableAB = models.CharField(max_length=8)
    category = models.CharField(max_length=64, default="")
    conutry = models.CharField(max_length=32,choices=country_choices, default="")
    formonth=models.DateField()
    visadate = models.CharField(max_length=128)
    pubdate = models.DateField()
    description = models.TextField()

    def __str__(self):
        return "Viss Bulletin."

##################################################
class case_status_lin_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_lin_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days

    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_msc_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_msc_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_src_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_src_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_wac_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_wac_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_eac_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_eac_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_ysc_lb(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_ysc_lb'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_lin_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_lin_sc'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_msc_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_msc_sc'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_src_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_src_sc'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_wac_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_wac_sc'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_eac_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_eac_sc'
            )
        ]
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

class case_status_ysc_sc(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_ysc_sc'
            )
        ]

    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days

    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"


class case_status_ioe(models.Model):
    receipt_number = models.CharField(max_length=16)
    form = models.CharField(max_length=16)
    status = models.CharField(max_length=128)
    action_date = models.CharField(max_length=32)
    action_date_x = models.DateField(default=date.today)
    case_stage = models.CharField(max_length=32,default="")
    rd_date = models.DateField('date received',default=date(2000,1,1))
    add_date = models.DateTimeField('date added')
    date_number = models.IntegerField()
    def action_days_to_now(self):
        days = (datetime.date(datetime.now()) - self.action_date_x).days
        return days
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['receipt_number', 'status','action_date'], name='unique_receipt_status_date_ioe'
            )
        ]

    def __str__(self):
        return f"Recepit Num: {self.receipt_number}\n" \
               f"Form: {self.form}\n" \
               f"Status: {self.status}\n" \
               f"Action date: {self.action_date}\n"

