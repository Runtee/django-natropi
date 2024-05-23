from django.contrib import admin
from .models import Transaction
# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'usdt_amount', 'transaction_type', 'description','created',  'verified')
    readonly_fields = ('profile', 'usdt_amount', 'transaction_type', 'description','created',  'verified')