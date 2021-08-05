import re
from django.db.models.fields import PositiveSmallIntegerField
# from connect.post.models import Post
from django.shortcuts import render
import inspect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import PostSerializers,CommentSerializers,LikeSerializers,PostSerializers1
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
from . models import Post,Comment,Like
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
# Create your views here.
from user.models import Users,Group
from friends.models import Friend
from django.db.models import Q
# Create your views here.
# create delet update Post
# get single user Post
# get friends PositiveSmallIntegerField
from notification.models import Notification
class Feed(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser)
    # parser_classes = [FileUploadParser]
    def get(self,requset):
        instance = Post.objects.filter(user__username = requset.user)
        # print(instance)
        serializer = PostSerializers(instance,many=True)
        return Response(serializer.data)
    def post(self,request):
        
        serializer = PostSerializers1(data=request.data)
        print(serializer.is_valid())
        print(serializer._errors)
        if(serializer.is_valid()):
            serializer.save()
            instance= Friend.objects.filter(Q(user2__username=request.user.username)| Q(user1__username=request.user.username))
            for ele in instance:
                if(ele.user1.username==request.user.username):
                    Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=ele.user2,Notification="Post Created from "+request.user.username,is_seen=False)
                else:
                    Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=ele.user1,Notification="Post Created from "+request.user.username,is_seen=False)
            return Response("Post Created sucessfully")
        return Response("Something went wronge")
    def delete(self,request):
        instance = Post.objects.get(id= request.data['id'])
        print(instance)
        instance.delete()
        return Response("Deleted sucessfull")
class PostAll(APIView):
    permission_classes = (IsAuthenticated,)
    
    # parser_classes = [FileUploadParser]
    def get(self,request):
        instance= Friend.objects.filter(Q(user2__username=request.user.username)| Q(user1__username=request.user.username))
        # if(user2__username==)
        User_data=[]
        for ele in instance:
            if(ele.user2.username==request.user.username):
                User_data.append(ele.user1)
            else:
                User_data.append(ele.user2)
        Post_data=[]
        for ele in User_data:
            instance = Post.objects.filter(user__username = ele.username)
            serializer = PostSerializers(instance,many=True)
            # print(Post_data)
            # print(instance)
            Post_data=Post_data+serializer.data
        # print(instance)
        
        return Response(Post_data)
class CommentApi(APIView):
    def get(self,request):
        try:
            instance = Comment.objects.get(post = request.data['id'])
        except ObjectDoesNotExist:
            return Response('No comments')
        serializer = CommentSerializers(instance,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serilizer = CommentSerializers(data=request.data)
        if (serilizer.is_valid()):
            serilizer.save()
            return Response('saved')
        return Response('Somthing went wrong')
    
    def delete(self,request):
        instance = Comment.objects.get(id=request.data['id'])
        instance.status=False
        instance.save()
        return Response('Deleted')
    
class LikeApi(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serilizer = LikeSerializers(data=request.data)
        if (serilizer.is_valid()):
            serilizer.save()
            # instance= Friend.objects.filter(Q(user2__username=request.user.username)| Q(user1__username=request.user.username))
            # for ele in instance:
                # if(ele.user1.username==request.user.username):
                    # Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=ele.user2,Notification="Post Created from "+request.user.username,is_seen=False)
                # else:
            instance=Post.objects.get(id=request.data['post'])
            Notification.objects.create(sender_user=User.objects.get(username=request.user.username),reciver_user=instance.user,Notification="Like from "+request.user.username+" on post",is_seen=False)
            return Response('saved')
        return Response('Somthing went wrong')
    def get(self,request):
        try:
            instance = Like.objects.get(post = request.data['id'])
        except ObjectDoesNotExist:
            return Response('No comments')
        serializer = Like(instance,many=True)
        return Response(serializer.data)
    def delete(self,request):
        instance = Like.objects.get(id=request.data['id'])
        # del instance
        instance.delete()
        # instance.save()
        return Response('Deleted')
    
class LikeApiUnique(APIView):
    
    def get(self,request,id):
        print(id)
        try:
            instance = Like.objects.filter(post__id = id)
        except ObjectDoesNotExist:
            return Response('No comments')
        serializer = LikeSerializers(instance,many=True)
        print(serializer.data)
        return Response(serializer.data)