from django.contrib import admin
from transfer.models import Transfer
# Register your models here.
@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('profile','transfer_profile','usdt_amount','transferred','created')
    readonly_fields = ('profile','transfer_profile','usdt_amount','transferred','created',)