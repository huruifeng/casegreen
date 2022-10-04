from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
]

app_name = 'ioe'
