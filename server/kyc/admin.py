from django.contrib import admin
from .models import Kyc
from django.utils.html import format_html
# Register your models here.

@admin.register(Kyc)
class KycAdmin(admin.ModelAdmin):
    list_display = ('profile','first_name', 'last_name','country', 'phone','ids_type', 'address','proof_of_address', 'created', 'verification_status')
    readonly_fields = ('verified',)

    def verification_status(self, obj):
        if not obj.verified:
            return format_html('<a href="/kyc/verify/{}" class="verify-link">Verify</a>', obj.id)
        else:
            return 'Verified'

    verification_status.short_description = 'Verification Status'
    verification_status.allow_tags = True
    verification_status.admin_order_field = 'verified'

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.verified:
            return ['profile','first_name', 'last_name','country', 'phone','ids_type', 'address','proof_of_address', 'created','verified', 'verification_status']
        return ['verified']
