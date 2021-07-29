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

# Create your views here.
# create delet update Post
# get single user Post
# get friends PositiveSmallIntegerField

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
            return Response("Post Created sucessfully")
        return Response("Something went wronge")
    def delete(self,request):
        instance = Post.objects.get(id= request.data['id'])
        print(instance)
        instance.delete()
        return Response("Deleted sucessfull")

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
    def post(self,request):
        serilizer = LikeSerializers(data=request.data)
        if (serilizer.is_valid()):
            serilizer.save()
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
        instance.status=False
        instance.save()
        return Response('Deleted')
    