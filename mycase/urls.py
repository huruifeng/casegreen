from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mycase/', views.mycase, name='mycase'),
    path('visabulletin/', views.visabulletin, name='visabulletin'),
    path('ajax/getjson', views.getjson, name = "getjson"),
    path('ajax/caseinrange', views.caseinrange, name = "caseinrange"),

]

app_name = 'mycase'