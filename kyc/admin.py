from django.contrib import admin
from .models import KYC

class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'document_number', 'verified', 'submitted_at')
    list_filter = ('verified', 'document_type', 'submitted_at')
    search_fields = ('user__username', 'document_number', 'document_type')
    ordering = ('-submitted_at',)

    def has_add_permission(self, request):
        # Prevent KYC from being added from the admin
        return False

admin.site.register(KYC, KYCAdmin)
