from django.urls import path, include
from django.contrib import admin
import django.core.handlers.wsgi
from . import views 

urlpatterns = [

path('',views.FriendAPI.as_view()),
path('chat/<int:id>',views.ChatAPI.as_view()),
path('search',views.SearchFriends.as_view()),
path('acceptrequest',views.AcceptRequest.as_view())
]