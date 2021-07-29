from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import ChatSerializer, FriendSerializer,FriendSerializer1
from django.contrib.auth.models import GroupManager, User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from user.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django import db
# Create your views here.
from user.models import Users,Group
from .models import Friend,Chat
# Create your views here.
# friend unfriend 
class FriendAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance= Friend.objects.filter(user1__username=request.user.username)
        serializer = FriendSerializer(instance,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=FriendSerializer1(data=request.data)
        
        if(serializer.is_valid()):
            print(serializer)
            serializer.save()
            return Response('friend request sent')
    def delete(self,request):
        instance = Friend.objects.get(user1__username=request.user,user2__id=request.data['id'])
        instance.delete()
        return Response('Deletion sucess full')
# get create chat

class ChatAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        # instance = Friend.objects.get(user1__username=request.user,user2__id=request.data['id'])
        inst = Chat.objects.get(friend__id=request.data['id'])
        serializer = ChatSerializer(inst,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=ChatSerializer(data=request.data)
        
        if(serializer.is_valid()):
            print(serializer.errors)
            serializer.save()
            return Response('message sent')

    def delete(self,request):
        instance = Chat.objects.get(id=request.data['id'])
        instance.delete()
        return Response('Deletion sucess full')
        
    
