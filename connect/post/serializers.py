from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post,Comment,Like
import user
class PostSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model= Post
        fields = '__all__'
    def get_user(self,obj):
        # print(type(obj))
        # print(User.objects.get(username=obj.user.username))
        return user.serializers.UserForeignKey(User.objects.get(username=obj.user.username),read_only=True).data
    # def post_user(self,obj):
    #     return User.objects.get(username=obj.user.username)
class PostSerializers1(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    
    class Meta:
        model= Post
        fields = '__all__'
    

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields = '__all__'

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model= Like
        fields = '__all__'