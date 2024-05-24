from django.contrib import admin
from transfer.models import Transfer
# Register your models here.
@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('user','transfer_user','usdt_amount','transferred','created')
    readonly_fields = ('user','transfer_user','usdt_amount','transferred','created',)