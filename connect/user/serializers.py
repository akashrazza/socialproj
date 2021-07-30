from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group,Users

class UserSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
class UserForeignKey(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','is_active','profile')

class SignSerializer(serializers.Serializer):
    
    password1 = serializers.CharField(max_length=50)
    password2 = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    def save(self, validated_data):
    
        
        user = User.objects.create_user(validated_data['username'],email= validated_data['email'],first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],password=validated_data['password1'])
        # print(user.__dict__)
        
        return user

class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model= Group
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    class Meta:
        model= Users
        fields = '__all__'
    def get_user(self,obj):
        # print(type(obj))
        # print(User.objects.get(username=obj.user.username))
        return UserForeignKey(User.objects.get(username=obj.user.username),read_only=True).data
    def get_group(self,obj):
        # print(type(obj))
        # print(User.objects.get(username=obj.user.username))
        return GroupSerializers(Group.objects.get(id = obj.group.id),read_only=True).data