from django.db import models

# Create your models here.

class WalletAddress(models.Model):
    bitcoin_address  = models.CharField(max_length=200,blank=True,null=True)
    litecoin_address  = models.CharField(max_length=200,blank=True,null=True)
    xrp_address  = models.CharField(max_length=200,blank=True,null=True)
    etherum_address  = models.CharField(max_length=200,blank=True,null=True)
    usdt_address  = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=100,default='Wallet Address')
    
    def __str__(self):
        return str(self.id)
    

class Acct(models.Model):
    method = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    acct_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.method
    
    class Meta:
        verbose_name = "Payment Account"
        verbose_name_plural = "Payment Accounts"