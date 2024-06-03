from django.contrib import admin
from .models import Transfer, P2PTransfer

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_wallet', 'to_wallet', 'amount', 'date')
    search_fields = ('user__username', 'from_wallet', 'to_wallet')
    list_filter = ('from_wallet', 'to_wallet', 'date')



@admin.register(P2PTransfer)
class P2PTransferAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_wallet', 'to_wallet', 'amount', 'date', 'recipient_email')
    search_fields = ('user__username', 'recipient_email', 'from_wallet', 'to_wallet')
    list_filter = ('date', 'from_wallet', 'to_wallet')
    ordering = ('-date',)
