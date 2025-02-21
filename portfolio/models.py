from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal, InvalidOperation
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.util import send_email

import threading


User = get_user_model()

# Create your models here.
class PortfolioAdd(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    header = models.CharField(max_length=255, blank=True, null=True)
    min_invest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    invest_time = models.CharField(max_length=255, blank=True, null=True)
    horizon = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    level_of_risk = models.CharField(max_length=255, blank=True, null=True)
    conservation = models.CharField(max_length=255, blank=True, null=True)
    short_term = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)
    port_stock1 = models.CharField(max_length=255, blank=True, null=True)
    port_stock2 = models.CharField(max_length=255, blank=True, null=True)
    port_stock3 = models.CharField(max_length=255, blank=True, null=True)
    port_stock4 = models.CharField(max_length=255, blank=True, null=True)
    port_weight1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_weight2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_weight3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_weight4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_returns1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_returns2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_returns3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    port_returns4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    status = models.CharField(max_length=255, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.min_invest = self.convert_to_decimal(self.min_invest)
        self.port_weight1 = self.convert_to_decimal(self.port_weight1)
        self.port_weight2 = self.convert_to_decimal(self.port_weight2)
        self.port_weight3 = self.convert_to_decimal(self.port_weight3)
        self.port_weight4 = self.convert_to_decimal(self.port_weight4)
        self.port_returns1 = self.convert_to_decimal(self.port_returns1)
        self.port_returns2 = self.convert_to_decimal(self.port_returns2)
        self.port_returns3 = self.convert_to_decimal(self.port_returns3)
        self.port_returns4 = self.convert_to_decimal(self.port_returns4)
        super().save(*args, **kwargs)

    def convert_to_decimal(self, value):
        if value is None or value == '':
            return Decimal('0.00')
        try:
            return Decimal(value)
        except InvalidOperation:
            return Decimal('0.00')

class PortfolioQuerySet(models.QuerySet):
    def order_by_latest(self):
        return self.order_by('-updated_at')

class PortfolioManager(models.Manager):
    def get_queryset(self):
        return PortfolioQuerySet(self.model, using=self._db).order_by_latest()

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    date = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    portfolioadd = models.ForeignKey(PortfolioAdd, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='1')
    days_passed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def calculate_weekly_profit(self):
        short_term_profit = (Decimal(self.amount) * Decimal(self.portfolioadd.short_term)) / 100
        total_weeks = self.get_horizon_weeks()
        return short_term_profit / total_weeks

    def get_horizon_weeks(self):
        months = int(self.portfolioadd.horizon)
        return months * 4  # approximate weeks in a month
    
    def get_horizon_days(self):
        weeks = int(self.portfolioadd.horizon)
        return weeks * 7 
    
    def get_remaining_days(self):
        total_days = self.get_horizon_days()
        return total_days - self.days_passed
    
    def get_maturity_date(self):
        return self.created_at + timedelta(days=self.get_horizon_days())
    
    
    def get_total_profit(self):
        total_weekly_profit = (self.days_passed // 7) * self.calculate_weekly_profit()
        return total_weekly_profit
    
    def get_cumulative_profit(self):
        total_profit = (Decimal(self.amount) * Decimal(self.portfolioadd.short_term)) / 100
        total_weekly_profit = (self.days_passed // 7) * self.calculate_weekly_profit()
        remaining_profit = total_profit - total_weekly_profit
        if self.status == '2':  # Investment completed
            return total_profit
        return total_weekly_profit

    def get_total_profit(self):
        total_profit = (Decimal(self.amount) * Decimal(self.portfolioadd.short_term)) / 100
        return total_profit

    def send_weekly_profit_email(self, profit):
        try:
            email_subject = 'Weekly Investment Profit Notification'
            email_body = (
                f"Dear {self.user.username},\n\n"
                f"We are pleased to inform you that you have earned a weekly profit of {profit}.\n\n"
                "Best regards,\n"
                "The Natropi Team"
            )
            email_thread = threading.Thread(target=send_email, args=(email_subject, email_body, self.user.email))
            email_thread.start()
        except Exception as e:
            print('Error in send_weekly_profit_email:', e)

    def send_completion_email(self, profit):
        try:
            email_subject = 'Investment Completion Notification'
            email_body = (
                f"Dear {self.user.username},\n\n"
                f"Your investment has reached its maturity. You have earned a total profit of {profit}. "
                "Your initial investment has been refunded to your portfolio balance.\n\n"
                "Best regards,\n"
                "The Natropi Team"
            )
            email_thread = threading.Thread(target=send_email, args=(email_subject, email_body, self.user.email))
            email_thread.start()
        except Exception as e:
            print('Error in send_completion_email:', e)

@receiver(post_save, sender=Portfolio)
def create_investment(sender, instance, created, **kwargs):
    if created:
        from .scheduler import schedule_investments
        schedule_investments()
