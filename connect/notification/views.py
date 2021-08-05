import re
from rest_framework import serializers
from payment.models import Payment, PaymentHistory
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import NotificationSerializer
from django.contrib.auth.models import GroupManager, User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from notification.models import Notification

class NotificationApi(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        instance=Notification.objects.filter(reciver_user__username=request.user.username)
        serializer=NotificationSerializer(instance,many=True)
        return Response(serializer.data)
    def post(self,request):
        for ele in request.data['data']:
            ins=Notification.objects.get(id=ele)
            ins.is_seen=True
            ins.save()
        return Response('Done')