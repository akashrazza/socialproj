# from connect.payment.models import Payment
# from connect import user
import inspect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import GroupSerializers, UserSerializer,SignSerializer,UsersSerializers
from django.contrib.auth.models import GroupManager, User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser
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
from payment.models import Payment
def emailFunction(sender, reciver, message):
    msg = message
    # send_mail('manufacturer Subject', 'Hi We you have new Order From eKnous Warehouse', 'shivam@eknous.com', [
    #     'anuj@eknous.com', email], fail_silently=False)
    send_mail('manufacturer Subject', msg,
              sender, [reciver], fail_silently=False)

    return HttpResponse('success')
######################################################################################
class Logout(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        ins=User.objects.get(username=request.user.username)
        ins.online=False
        ins.save()
        return Response('logout sucessfull')
class auth(APIView):
    
    
    permission_classes = (IsAuthenticated,)
    # print(permission_classes)
    
    def get(self,request):
        
        user = User.objects.get(username=request.user.username)
        # print(user)
        user.online=True
        user.save()
        serializer= UserSerializer({'username':user.username,'email':user.email,'firstname':user.first_name,'lastname':user.last_name,'id':user.id,'profile':user.profile})
        
        return Response(serializer.data)

class Signup(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)
    def post(self,request):
        data=request.data
        
        if(data['password1']==data['password2']):
            # print('1')
            serializer=SignSerializer(data=request.data)
            # print('2',serializer.is_valid())
            if(serializer.is_valid()):
                try:
                    user=User.objects.get(username=request.data['username'])
                    return Response({'user already exists'})
                except ObjectDoesNotExist:
                    pass
                # print(serializer)
                user=serializer.save(data)
                mail_subject = 'Activate your OrderMange UserAccount.'
                # print(user)
                message = render_to_string('email.html', {
                    'user': user,
                    'domain': 'http://127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),                    
                })
                to_email = request.data['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                # print(email)
                email.send()
                Payment.objects.create(user=user,balance=0)
                return Response({'User Created sucessfully'})
        return Response(serializer.errors)

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# create group
class GroupCreate(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer = GroupSerializers(data=request.data)
        print(serializer.is_valid())
        if(serializer.is_valid()):
            instance = serializer.save()
            # print(instance)
            a=Users.objects.create(group = instance ,user = User.objects.get(username=request.user))
            return Response("created")
    def delete(self,request):
        instance = Group.objects.get(id=request.data['id'])
        del instance
        return Response('Deleted Sucessfull')
class ListOfGroupFromUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance = Users.objects.filter(user__username=request.user)
        print(instance)
        serializer = UsersSerializers(instance,many=True)
        
        return Response(serializer.data)
    
class ListOfUserFromGroup(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        instance = Users.objects.get(group__id=request.data['id'])
        print(instance)
        serializer = UsersSerializers(instance)
        
        return Response(serializer.data)
    def delete(self,request):
        instance = Users.objects.get(group__id=request.data['id'],user__username=request.data['username'])
        del instance
        return Response("Deleted Sucessfully")


# class AddUserToGroup(APIView):
#     def post(self,request):


# update group details
