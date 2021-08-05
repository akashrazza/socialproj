from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notification.models import Notification
# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    model = Notification

    list_display = '__all__'


admin.site.register(Notification)
