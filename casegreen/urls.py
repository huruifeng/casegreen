"""casegreen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.mycase, name='mycase')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='mycase')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('huadmin/', admin.site.urls,name="huadmin"),
    path("accounts/", include("django.contrib.auth.urls"),name="login"),  # new
    path('', include('mycase.urls',namespace="casegreen"),name="home"),
    path('mycase/', include('mycase.urls',namespace="mycase"),name="home"),
    path('ctrlpanel/', include('ctrlpanel.urls',namespace="ctrlpanel"),name="home"),

]
app_name = 'casegreen'
