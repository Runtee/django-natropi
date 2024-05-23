from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    pass
