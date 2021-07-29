from django.urls import path, include
from django.contrib import admin
import django.core.handlers.wsgi
from . import views 
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
path('activate/<uidb64>/<token>/',views.activate,name='activate'),
path('apitoken/', obtain_auth_token, name='api_token_auth'),
path('api/',views.auth.as_view()),
path('api/signup/',views.Signup.as_view()),
path('api/groups/',views.GroupCreate.as_view()),

path('api/listofgroupfromuser/',views.ListOfGroupFromUser.as_view()),
path('api/listofuserfromgroup/',views.ListOfUserFromGroup.as_view()),
]


"""for Lodaing Static files in django """

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""End Of  Lodaing Static files in django """