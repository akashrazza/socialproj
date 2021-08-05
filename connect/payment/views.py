import re
from rest_framework import serializers
from payment.models import Payment, PaymentHistory
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import PaymentHistorySerializer,PaymentSerializer
from django.contrib.auth.models import GroupManager, User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from notification.models import Notification
# Create your views here.
class PaymentAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance=Payment.objects.get(user__username=request.user.username)
        serializer=PaymentSerializer(instance)
        return Response(serializer.data)
    def post(self,request):
        serializer=PaymentSerializer(data=request.data)
        # print(serializer.errors)
        if(serializer.is_valid()):
            # print(serializer)
            # serializer.save()
            instance=Payment.objects.get(user__username=request.user.username)
            if(int(instance.balance+int(request.data['balance']))<0):
                return Response('not have enough balance')
            instance.balance=instance.balance+int(request.data['balance'])
            instance.save()
            # ins=User.objects.get(username=request.user.username)
            PaymentHistory.objects.create(main_account=instance.user,user_account=instance.user,perform="Amount Added "+str(request.data['balance']))
            # Notification.objects.create(sender_user=instance,reciver_user=reciver,Notification="Message recived from "+request.user.username,is_seen=True if reciver.online else False)
            return Response('Amount added')
class PaymentTransferApi(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer = PaymentSerializer(data=request.data)
        if(serializer.is_valid()):
            instance1=Payment.objects.get(user__username=request.user.username)
            if(instance1.balance<int(request.data['balance'])):
                return Response("not have enough balance")

            instance1.balance=instance1.balance-int(request.data['balance'])
            instance1.save()

            ins=User.objects.get(id=request.data['user'])
            instance=Payment.objects.get(user__username=ins.username)
            instance.balance=instance.balance+int(request.data['balance'])
            instance.save()
            # ins1=User.objects.get(user__username=request.user.username)
            PaymentHistory.objects.create(main_account=instance.user,user_account=instance1.user,perform="Amount transferd "+str(request.data['balance'])+" from "+request.user.username)
            PaymentHistory.objects.create(main_account=instance1.user,user_account=ins,perform="Amount transfered "+str(request.data['balance'])+" to "+ins.username)
            Notification.objects.create(sender_user=instance1.user,reciver_user=ins,Notification="Payment recived "+str(request.data['balance'])+" from "+request.user.username,is_seen=False)
            return Response('Amount added')
class PaymentHistoryApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance=PaymentHistory.objects.filter(main_account__username=request.user.username)
        serializer=PaymentHistorySerializer(instance,many=True)
        return Response(serializer.data)