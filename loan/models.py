from django.db import models

class LoanTerm(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1: $50,000 to $500,000'),
        ('Term 2', 'Term 2: $1,000,000 or more'),
    ]

    term_name = models.CharField(max_length=50, choices=TERM_CHOICES)

    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)

    interest_rate_min = models.DecimalField(max_digits=5, decimal_places=2)
    interest_rate_max = models.DecimalField(max_digits=5, decimal_places=2)

    repayment_term_min = models.IntegerField(help_text="Minimum repayment term in months")
    repayment_term_max = models.IntegerField(help_text="Maximum repayment term in months")

    repayment_frequency = models.CharField(max_length=50, default="Monthly")

    origination_fee_min = models.DecimalField(max_digits=5, decimal_places=2)
    origination_fee_max = models.DecimalField(max_digits=5, decimal_places=2)

    late_payment_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    late_payment_fee_fixed = models.DecimalField(max_digits=10, decimal_places=2)

    prepayment_penalty = models.BooleanField(default=False)
    default_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    collateral_required = models.BooleanField(default=False)
    credit_score_min = models.IntegerField()
    income_requirement_personal = models.DecimalField(max_digits=10, decimal_places=2)
    income_requirement_business = models.DecimalField(max_digits=10, decimal_places=2)
    debt_to_income_ratio_max = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.term_name
