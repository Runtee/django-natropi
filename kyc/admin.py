from django.contrib import admin
from .models import KYC

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__username', 'document_number')
    list_editable = ('status',)  # Make the 'status' field editable in the list view
