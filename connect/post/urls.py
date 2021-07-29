from django.urls import path, include
from django.contrib import admin
import django.core.handlers.wsgi
from . import views 
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [

path('',views.Feed.as_view()),
path('comment',views.CommentApi.as_view()),
]