from django.contrib import admin
from user.models import Group,Users
# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    model = Group
    list_display = ['name']


admin.site.register(Group, GroupsAdmin)

class UsersAdmin(admin.ModelAdmin):
    model = Users
    list_display = ['user','group']


admin.site.register(Users, UsersAdmin)