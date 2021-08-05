from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Notification

class UserForeignKey(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','is_active','online','profile')
class NotificationSerializer(serializers.ModelSerializer):
    sender_user= serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = '__all__'
    def get_sender_user(self,obj):
        # print(type(obj))
        # print(obj.__dict__)
        # print(User.objects.get(username=obj.user.username))
        return UserForeignKey(User.objects.get(id=obj.sender_user.id),read_only=True).data