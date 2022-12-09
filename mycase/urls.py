from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mycase/', views.mycase, name='mycase'),
    path('dashborddaily/', views.dashborddaily, name='dashborddaily'),
    path('dashbordajax/', views.dashbordajax, name='dashbordajax'),
    path('overview/', views.overview, name='overview'),
    path('processrn/', views.processrn, name='processrn'),
    path('processrd/', views.processrd, name='processrd'),
    path('summaryrn/', views.processrn, name='summaryrn'),
    path('summaryrd/', views.processrd, name='summaryrd'),
    path('processajax/', views.processajax, name='processajax'),
    path('countscalendar/', views.countscalendar, name='countscalendar'),
    path('query/', views.query, name='query'),
    path('today/', views.todaycounts, name='today'),
    path('nextstatus/', views.nextstatus, name='nextstatus'),
    path('about/', views.about, name='about'),

    path('ajax/caseinrange', views.caseinrange, name = "caseinrange"),
    path('ajax/mynextstatus', views.mynextstatus, name = "mynextstatus"),
    path('ajax/dailyrecords', views.dailyrecords, name = "dailyrecords"),
    path('ajax/rnrangecount', views.rnrangecount, name = "rnrangecount"),
    path('ajax/getsankey', views.getsankey, name = "getsankey"),
    path('ajax/todaymodalcasetable', views.todaymodalcasetable, name = "todaymodalcasetable"),

]

app_name = 'mycase'
