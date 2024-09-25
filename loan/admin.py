from django.contrib import admin
from .models import LoanTerm, LoanApplication, Upfront, Loan

# Admin configuration for LoanTerm model
@admin.register(LoanTerm)
class LoanTermAdmin(admin.ModelAdmin):
    list_display = ('term_name', 'min_amount', 'max_amount', 'interest_rate_min', 'interest_rate_max', 'repayment_term_min', 'repayment_term_max', 'collateral_required')
    list_filter = ('term_name', 'collateral_required')
    search_fields = ('term_name',)
    ordering = ('term_name',)

# Admin configuration for LoanApplication model
@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_term', 'loan_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'loan_term__term_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

# Admin configuration for Upfront model
@admin.register(Upfront)
class UpfrontAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'transaction_hash', 'loan_amount_requested', 'date')
    list_filter = ('method', 'date')
    search_fields = ('user__username', 'transaction_hash')
    ordering = ('-date',)
    readonly_fields = ('date',)

# Admin configuration for Loan model
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_requested', 'amount_paid', 'remaining_balance', 'remaining_months', 'applied_date')
    list_filter = ('applied_date',)
    search_fields = ('user__username',)
    ordering = ('-applied_date',)
    readonly_fields = ('upfront_payment', 'remaining_balance', 'remaining_months')

    # Customize the display of Many-to-Many field (upfronts)
    filter_horizontal = ('upfronts',)
