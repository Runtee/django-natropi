from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Acct)
class AcctAdmin(admin.ModelAdmin):
    pass