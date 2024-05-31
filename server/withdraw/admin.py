from django.contrib import admin
from .models import Account, WithdrawalsMade
from django.utils.html import format_html
# Register your models here.


admin.site.register(Account)

@admin.register(WithdrawalsMade)
class WithdrawalsMadeAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_type', 'amount', 'method', 'date', 'is_verified']
    list_filter = ['is_verified', 'date']
    search_fields = ['user__username', 'wallet_type']
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected withdrawals have been marked as verified.")
    mark_as_verified.short_description = "Mark selected withdrawals as verified"