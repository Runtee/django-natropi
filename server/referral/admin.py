from django.contrib import admin
from .models import Referral

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred_user', 'referral_code', 'referral_count', 'referral_bonus', 'created_at', 'updated_at')
    search_fields = ('referrer__username', 'referred_user__username', 'referral_code')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Referral, ReferralAdmin)
