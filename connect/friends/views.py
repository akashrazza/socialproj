from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import ChatSerializer, FriendSerializer,FriendSerializer1, GetChatSerializer,SearchSerializer
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
from django.db.models import Q
from user.serializers import UserForeignKey
from notification.models import Notification
# Create your views here.
# friend unfriend 
class FriendAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance= Friend.objects.filter(Q(user2__username=request.user.username)| Q(user1__username=request.user.username))
        # print(type(instance))
        # instance=Friend.objects.filter(user1__username=request.user.username)
        serializer = FriendSerializer(instance,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=FriendSerializer1(data=request.data)
        
        if(serializer.is_valid()):
            print(serializer)
            serializer.save()
            Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=User.objects.get(id=request.data['user2']),Notification="Freiend request recived from "+request.user.username)
            return Response('friend request sent')
    def delete(self,request):
        instance = Friend.objects.get(user1__username=request.user,user2__id=request.data['id'])
        instance.delete()
        return Response('Deletion sucess full')
# get create chat
class AcceptRequest(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance= Friend.objects.filter( user2__username=request.user.username)
        # print(type(instance))
        # instance=Friend.objects.filter(user1__username=request.user.username)
        serializer = FriendSerializer(instance,many=True)
        return Response(serializer.data)
    def post(self,request):
        id=request.data['id']
        obj=Friend.objects.get(id=id)
        obj.status=True
        obj.save()
        Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=obj.user1,Notification="Freiend request accepted from "+request.user.username)
        return Response("ok")
    def delete(self,request):
        id=request.data['id']
        obj=Friend.objects.get(id=id)
        obj.delete()
        return Response("ok")

class SearchFriends(APIView):
    def post(self,request):
        searilizer = SearchSerializer(data=request.data)
        if(searilizer.is_valid()):
            instance= Friend.objects.filter(Q(user2__username=request.user.username)| Q(user1__username=request.user.username))
            context = User.objects.filter(username__icontains=request.data['query'] )
            s = UserForeignKey(context,many=True)
            return Response(s.data)
        else:
            return Response("nothing found")
class SearchFriendsaccept(APIView):
    def post(self,request):
        searilizer = SearchSerializer(data=request.data)
        if(searilizer.is_valid()):
            context = Friend.objects.filter(username__icontains=request.data['query'] )
            s = UserForeignKey(context,many=True)
            return Response(s.data)
        else:
            return Response("nothing found")
class ChatAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id):
        # instance = Friend.objects.get(user1__username=request.user,user2__id=request.data['id'])
        inst = Chat.objects.filter(friend__id=id)
        serializer = GetChatSerializer(inst,many=True)
        return Response(serializer.data)
    def post(self,request,id):
        serializer=ChatSerializer(data=request.data)
        
        if(serializer.is_valid()):
            print(serializer.errors)
            serializer.save()
            ins=Friend.objects.get(id=request.data['friend'])
            if(ins.user1.id==request.data['sender']):
                reciver=ins.user2
                sender=ins.user1
            else:
                reciver=ins.user1
                sender=ins.user2
            Notification.objects.create(sender_user=reciver,reciver_user=sender,Notification="Message recived from "+request.user.username,is_seen=False)
            return Response('message sent')

    def delete(self,request):
        instance = Chat.objects.get(id=request.data['id'])
        instance.delete()
        return Response('Deletion sucess full')
        
    
