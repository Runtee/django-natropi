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