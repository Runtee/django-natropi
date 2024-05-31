from django.contrib import admin
from .models import Withdrawal, Account, WithdrawalsMade
from django.utils.html import format_html
# Register your models here.

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount', 'verification_status')
    readonly_fields = ('verified',)

    def verification_status(self, obj):
        if not obj.verified:
            return format_html('<a href="/withdraw/verify/{}" class="verify-link">Verify</a>', obj.id)
        else:
            return 'Verified'

    verification_status.short_description = 'Verification Status'
    verification_status.allow_tags = True
    verification_status.admin_order_field = 'verified'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.verified:
            return ['verified', 'user', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount']
        return ['verified']
    
admin.site.register(Account)
admin.site.register(WithdrawalsMade)