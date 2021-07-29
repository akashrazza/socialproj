from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from user.models import Group

class Friend(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')
    status = models.BooleanField()
    date_time = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    friend = models.ForeignKey(Friend,on_delete=models.CASCADE,null=True,default='')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,default='')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    message =  models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)

