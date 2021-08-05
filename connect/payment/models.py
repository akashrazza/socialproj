from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    balance=models.IntegerField()
class PaymentHistory(models.Model):
    main_account=models.ForeignKey(User,on_delete=models.CASCADE,related_name='main_account')
    user_account=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_account')
    perform=models.TextField(max_length=100)
    date_time=models.DateField(auto_now_add=True)
    

    