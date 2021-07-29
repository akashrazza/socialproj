from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    post_name = models.CharField(max_length=200)
    post_file_name = models.FileField( upload_to='media')
    time_date = models.DateTimeField(auto_now_add=True)
    dsec = models.CharField(max_length=500)

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField()
    message = models.CharField(max_length=500)