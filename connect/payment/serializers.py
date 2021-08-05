from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PaymentHistory,Payment
# import user
class UserForeignKey(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','is_active','online','profile')
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentHistorySerializer(serializers.ModelSerializer):
    main_account = serializers.SerializerMethodField()
    user_account = serializers.SerializerMethodField()
    class Meta:
        model = PaymentHistory
        fields = '__all__'
    def get_main_account(self,obj):
        # print(type(obj))
        # print(obj.__dict__)
        # print(User.objects.get(username=obj.user.username))
        return UserForeignKey(User.objects.get(id=obj.main_account.id),read_only=True).data
    def get_user_account(self,obj):
        # print(type(obj))
        # print(obj.__dict__)
        # print(User.objects.get(username=obj.user.username))
        return UserForeignKey(User.objects.get(id=obj.user_account.id),read_only=True).data