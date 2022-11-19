from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ctrlhome'),
    path('dashbord/', views.ctrl_dashbord, name='ctrldashbord'),
    path('login/', views.login_view, name='ctrllogin'),
    path('exportdb/', views.exportDB, name='ctrlexportdb'),
    path('checkcase/', views.checkcase, name='ctrlcheckcase'),

    path('checkcase/checkcase_query', views.checkcase_query, name='checkcase_query'),
    path('checkcase/checkcase_update', views.checkcase_update, name='checkcase_update'),
    path('checkcase/checkcase_del', views.checkcase_del, name='checkcase_del'),

    path('ajax/sysupdate', views.sysupdate, name='sysupdate'),
    path('ajax/centerrun', views.centerrun, name='centerrun'),
    path('ajax/sysinit', views.sysinit, name='sysinit'),
    path('ajax/centerstatus', views.centerstatus, name='centerstatus'),

]

app_name = 'ctrlpanel'
