from django.contrib import admin
from .models import WithdrawalsMade
from django.utils.html import format_html

@admin.register(WithdrawalsMade)
class WithdrawalsMadeAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_type', 'amount', 'method', 'date', 'verification_status')
    readonly_fields = ('is_verified',)
    list_filter = ['is_verified', 'date']
    search_fields = ['user__username', 'wallet_type']
    actions = ['mark_as_verified']

    def verification_status(self, obj):
        if not obj.is_verified:
            return format_html('<a href="/withdraw/verify/{}" class="verify-link">Verify</a>', obj.id)
        else:
            return 'Verified'

    verification_status.short_description = 'Verification Status'
    verification_status.allow_tags = True
    verification_status.admin_order_field = 'is_verified'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_verified:
            return ['is_verified', 'user', 'wallet_type', 'amount', 'method', 'date']
        return ['is_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
        self.message_user(request, "Selected withdrawals have been marked as verified.")

    mark_as_verified.short_description = "Mark selected withdrawals as verified"
