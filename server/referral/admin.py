from django.contrib import admin
from .models import Referral
# Register your models here.
@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    pass