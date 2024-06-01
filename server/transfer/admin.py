from django.contrib import admin
from .models import Transfer

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_wallet', 'to_wallet', 'amount', 'date')
    search_fields = ('user__username', 'from_wallet', 'to_wallet')
    list_filter = ('from_wallet', 'to_wallet', 'date')
