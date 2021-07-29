from django.contrib import admin
from friends.models import Friend,Chat
# Register your models here.


class FriendsAdmin(admin.ModelAdmin):
    model = Friend
    list_display = ['user1','user2','status','date_time']


admin.site.register(Friend, FriendsAdmin)


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['friend','group','sender','message','date_time']


admin.site.register(Chat, ChatAdmin)