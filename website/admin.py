from django.contrib import admin
from .models import *
from .util import project
# Register your models here.

@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('owned_by','name','email','address','second_address','logo','phone_number')
    list_editable = ('name','email','address','second_address','logo','phone_number')
    list_display_links = ('owned_by',)
    

admin.site.site_header = project
admin.site.site_title = project
admin.site.index_title = f"Welcome to {project} Portal"

