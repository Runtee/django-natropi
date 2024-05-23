from django.contrib import admin
from .models import Deposit
from django.utils.html import format_html
# Register your models here.

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount', 'verification_status')
    readonly_fields = ('verified',)

    def verification_status(self, obj):
        if not obj.verified:
            return format_html('<a href="/deposit/verify/{}" class="verify-link">Verify</a>', obj.id)
        else:
            return 'Verified'

    verification_status.short_description = 'Verification Status'
    verification_status.allow_tags = True
    verification_status.admin_order_field = 'verified'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.verified:
            return ['verified', 'profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount']
        return ['verified']

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions








# @admin.register(Deposit)
# class DepositAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount', 'verified', 'verify_transaction')
#     readonly_fields = ('verified',)

#     def verify_transaction(self, obj):
#         if not obj.verified:
#             return format_html('<a href="{}">Verify</a>').format(obj.id)
#         else:
#             return 'Verified'

#     verify_transaction.short_description = 'Verification Status'
#     verify_transaction.allow_tags = True
#     verify_transaction.admin_order_field = 'verified'

#     def save_model(self, request, obj, form, change):
#         if not obj.verified:
#             obj.verified = True
#             obj.save()

#     def get_readonly_fields(self, request, obj=None):
#         if obj and obj.verified:
#             return ['verified', 'profile', 'wallet_address', 'amount', 'wallet_type', 'created', 'usdt_amount']
#         return ['verified']

#     def get_actions(self, request):
#         actions = super().get_actions(request)
#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
        
    




