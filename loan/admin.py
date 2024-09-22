from django.contrib import admin
from .models import LoanTerm

class LoanTermAdmin(admin.ModelAdmin):
    list_display = ('term_name', 'min_amount', 'max_amount', 'interest_rate_min', 'interest_rate_max', 'repayment_term_min', 'repayment_term_max', 'credit_score_min')
    list_filter = ('term_name', 'repayment_frequency', 'credit_score_min', 'collateral_required')
    search_fields = ('term_name', 'min_amount', 'max_amount', 'credit_score_min')
    fieldsets = (
        (None, {
            'fields': ('term_name', 'min_amount', 'max_amount')
        }),
        ('Interest & Repayment', {
            'fields': ('interest_rate_min', 'interest_rate_max', 'repayment_term_min', 'repayment_term_max', 'repayment_frequency')
        }),
        ('Fees', {
            'fields': ('origination_fee_min', 'origination_fee_max', 'late_payment_fee_percentage', 'late_payment_fee_fixed')
        }),
        ('Other Details', {
            'fields': ('prepayment_penalty', 'default_interest_rate', 'collateral_required', 'credit_score_min', 'income_requirement_personal', 'income_requirement_business', 'debt_to_income_ratio_max')
        }),
    )

admin.site.register(LoanTerm, LoanTermAdmin)
