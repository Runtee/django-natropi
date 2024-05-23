from django.db import models
from userprofile.models import Profile
# Create your models here.

class Withdrawal(models.Model):
    WALLETTYPECHOICES = (
       ('USDT', 'USDT'),
        ('LTC', 'Litecoin'),
        ('BTC', 'Bitcoin'),
        ('XRP','XRP'),
        ('ETH','ETHERUM'),
    )
     
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='withdrawal')
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    wallet_type  = models.CharField(choices=WALLETTYPECHOICES,max_length=10,blank=True,null=True)
    wallet_address = models.CharField(max_length=100,blank=True,null=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.profile.user.get_username} was withdrawn {self.usdt_amount} in {self.wallet_address}'
    
    def save(self, *args, **kwargs):
        if self.verified == True:
            self.profile.available_balance -=  float(self.usdt_amount)
            action = f'Your deposit of {self.amount} {self.wallet_type} into {self.wallet_address} is verified'
            self.profile.notification_set.create(profile=self.profile,action='Verified',description=f'Your deposit of {self.amount} {self.wallet_type} into {self.wallet_address} have been verified')
            self.profile.transaction_set.create(profile=self.profile, transaction_type='withdrawal', usdt_amount=self.usdt_amount, description=action,verified=True)
            self.profile.save() 
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.verified == True:
            self.profile.available_balance +=  float(self.usdt_amount)
            self.profile.save()  
        return super().delete(*args, **kwargs)