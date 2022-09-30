from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mycase/', views.mycase, name='mycase'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('process/', views.process, name='process'),
    path('today/', views.today, name='today'),
    path('about/', views.about, name='about'),
    path('visabulletin/', views.visabulletin, name='visabulletin'),
    path('ajax/caseinrange', views.caseinrange, name = "caseinrange"),
    path('ajax/nextstatus', views.nextstatus, name = "nextstatus"),
    path('ajax/dailyrecords', views.dailyrecords, name = "dailyrecords"),
    path('ajax/rnrangecount', views.rnrangecount, name = "rnrangecount"),

]

app_name = 'mycase'