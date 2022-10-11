from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mycase/', views.mycase, name='mycase'),
    path('dashborddaily/', views.dashborddaily, name='dashborddaily'),
    path('dashbordajax/', views.dashbordajax, name='dashbordajax'),
    path('processrn/', views.processrn, name='processrn'),
    path('processrd/', views.processrd, name='processrd'),
    path('processajax/', views.processajax, name='processajax'),
    path('today/', views.today, name='today'),
    path('about/', views.about, name='about'),

    path('visabulletin/', views.visabulletin, name='visabulletin'),
    path('ajax/caseinrange', views.caseinrange, name = "caseinrange"),
    path('ajax/nextstatus', views.nextstatus, name = "nextstatus"),
    path('ajax/dailyrecords', views.dailyrecords, name = "dailyrecords"),
    path('ajax/rnrangecount', views.rnrangecount, name = "rnrangecount"),
    path('ajax/getsankey', views.getsankey, name = "getsankey"),

]

app_name = 'mycase'
