from django.urls import path, include
from django.contrib import admin
import django.core.handlers.wsgi
from . import views 

urlpatterns = [

path('',views.PaymentAPI.as_view()),
path('transfer',views.PaymentTransferApi.as_view()),
path('paymenthistory',views.PaymentHistoryApi.as_view()),

]