from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

from decimal import Decimal, InvalidOperation

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
    portfolioadd = models.ForeignKey('PortfolioAdd', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PortfolioManager()
    def __str__(self):
        return self.user.get_username()
