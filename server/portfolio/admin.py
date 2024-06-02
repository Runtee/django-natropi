from django.contrib import admin
from .models import PortfolioAdd, Portfolio

class PortfolioAddAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'header', 'min_invest', 'invest_time', 'horizon', 'term', 'level_of_risk', 'conservation', 'short_term', 'status', 'created_at', 'updated_at')
    list_filter = ('type', 'term', 'level_of_risk', 'status')
    search_fields = ('name', 'type', 'header')
    readonly_fields = ('created_at', 'updated_at')

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'portfolioadd', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'date', 'portfolioadd')
    search_fields = ('user__username', 'portfolioadd__name')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(PortfolioAdd, PortfolioAddAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
