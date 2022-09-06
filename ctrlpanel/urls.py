from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ctrlhome'),
    path('dashbord/', views.ctrl_dashbord, name='ctrldashbord'),
    path('login/', views.login_view, name='login'),
    path('exportdb/', views.exportDB, name='exportdb'),
    path('visabulletin/', views.visabulletin, name='ctrlvisabulletin'),

    path('ajax/sysupdate', views.sysupdate, name='sysupdate'),
    path('ajax/centerrun', views.centerrun, name='centerrun'),
    path('ajax/sysinit', views.sysinit, name='sysinit'),
    path('ajax/centerstatus', views.centerstatus, name='centerstatus'),

]

app_name = 'ctrlpanel'
