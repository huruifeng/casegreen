from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('mycase/', views.mycase, name='mycase'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('today/', views.today, name='today'),
    path('about/', views.about, name='about'),
    path('visabulletin/', views.visabulletin, name='visabulletin'),
    path('ajax/caseinrange', views.caseinrange, name = "caseinrange"),

]

app_name = 'mycase'