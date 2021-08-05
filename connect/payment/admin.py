from django.contrib import admin
from payment.models import Payment,PaymentHistory
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ['user','balance']


admin.site.register(Payment, PaymentAdmin)


class PaymentHistoryAdmin(admin.ModelAdmin):
    model = PaymentHistory
    list_display = ['main_account','user_account','perform','date_time']


admin.site.register(PaymentHistory, PaymentHistoryAdmin)
