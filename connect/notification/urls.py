from django.urls import path, include
from django.contrib import admin
import django.core.handlers.wsgi
from . import views 

urlpatterns = [

path('',views.NotificationApi.as_view()),

]