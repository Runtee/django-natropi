from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'read', 'created')
    list_filter = ('read', 'created')
    search_fields = ('user__email', 'action', 'description')
    ordering = ('-created',)


admin.site.register(Notification, NotificationAdmin)

