from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friend,Chat
import user
class UserForeignKey(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','is_active')

class FriendSerializer(serializers.ModelSerializer):
    user2 = serializers.SerializerMethodField()
    class Meta:
        model = Friend
        fields = '__all__'
    def get_user2(self,obj):
        print(type(obj))
        print(obj.__dict__)
        # print(User.objects.get(username=obj.user.username))
        return UserForeignKey(User.objects.get(id=obj.user2.id),read_only=True).data
    # def post_user(self,obj):
    #     print(obj)
    #     return User.objects.get(username=obj.user.username)
class FriendSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = Friend
        fields = '__all__'
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'