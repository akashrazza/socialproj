from django.db import models
# from django.
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
# Create your models here.
class Notification(models.Model):
    sender_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender_name')
    reciver_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciver_name')
    Notification=models.CharField(max_length=1000)
    is_seen=models.BooleanField(default=False)
    date_time=models.DateTimeField(auto_now_add=True)
