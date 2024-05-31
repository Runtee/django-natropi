from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class PortfolioAdd(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    header = models.CharField(max_length=255, blank=True, null=True)
    min_invest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invest_time = models.CharField(max_length=255, blank=True, null=True)
    horizon = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    level_of_risk = models.CharField(max_length=255, blank=True, null=True)
    conservation = models.CharField(max_length=255, blank=True, null=True)
    short_term = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)
    port_stock1 = models.CharField(max_length=255, blank=True, null=True)
    port_stock2 = models.CharField(max_length=255, blank=True, null=True)
    port_stock3 = models.CharField(max_length=255, blank=True, null=True)
    port_stock4 = models.CharField(max_length=255, blank=True, null=True)
    port_weight1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_weight2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_weight3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_weight4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_returns1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_returns2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_returns3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    port_returns4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=255, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='portfoiles')
    date = models.CharField(max_length=255)
    amount = models.BigIntegerField()
    portfolioadd = models.ForeignKey(PortfolioAdd,on_delete=models.CASCADE)
    staamounttus = models.CharField(max_length=255, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()
