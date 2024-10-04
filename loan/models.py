from django.db import models
from accounts.models import CustomUser as User
from datetime import datetime, timedelta



class LoanTerm(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1: $50,000 to $500,000'),
        ('Term 2', 'Term 2: $1,000,000 or more'),
    ]

    term_name = models.CharField(max_length=50, choices=TERM_CHOICES)

    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=20, decimal_places=2)

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
    


class LoanApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_term = models.ForeignKey(LoanTerm, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)



class Upfront(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100)
    transaction_hash = models.CharField(max_length=255)
    loan_amount_requested = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.method}"
    

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    repayment_term_months = models.IntegerField()
    applied_date = models.DateField(default=datetime.now)
    upfronts = models.ManyToManyField('Upfront', related_name='loans', blank=True)

    @property
    def upfront_payment(self):
        return sum(upfront.amount for upfront in self.upfronts.all())

    @property
    def remaining_balance(self):
        return self.amount_requested - self.upfront_payment - self.amount_paid

    @property
    def remaining_months(self):
        end_date = self.applied_date + timedelta(days=self.repayment_term_months * 30)
        remaining_days = (end_date - datetime.now().date()).days
        return max(0, remaining_days // 30)

    def __str__(self):
        return f'Loan for {self.user.username} - Amount Requested: {self.amount_requested}'