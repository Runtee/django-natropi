from django.db import models
from accounts.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal
from django.conf import settings


# Create your models here.

class Withdrawal(models.Model):
    WALLETTYPECHOICES = (
       ('USDT', 'USDT'),
        ('LTC', 'Litecoin'),
        ('BTC', 'Bitcoin'),
        ('XRP','XRP'),
        ('ETH','ETHERUM'),
    )
     
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='withdrawal')
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    wallet_type  = models.CharField(choices=WALLETTYPECHOICES,max_length=10,blank=True,null=True)
    wallet_address = models.CharField(max_length=100,blank=True,null=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.get_username} was withdrawn {self.usdt_amount} in {self.wallet_address}'
    
    def save(self, *args, **kwargs):
        if self.verified == True:
            self.user.main -=  float(self.usdt_amount)
            action = f'Your deposit of {self.amount} {self.wallet_type} into {self.wallet_address} is verified'
            self.user.notification_set.create(user=self.user,action='Verified',description=f'Your deposit of {self.amount} {self.wallet_type} into {self.wallet_address} have been verified')
            self.user.transaction_set.create(user=self.user, transaction_type='withdrawal', usdt_amount=self.usdt_amount, description=action,verified=True)
            self.user.save() 
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.verified == True:
            self.user.main +=  float(self.usdt_amount)
            self.user.save()  
        return super().delete(*args, **kwargs)
    

class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    main_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    portfolio_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    strategy_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trade_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
    

class WithdrawalsMade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wallet_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    @property
    def status(self):
        return "verified" if self.is_verified else "pending"

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
    
    
@receiver(post_save, sender=Withdrawal)
def send_withdrawal_email(sender, instance, created, **kwargs):
    if created:
        # Send email for withdrawal received
        subject = 'Withdrawal Received - Pending Processing'
        html_message = None
        plain_message = f"Dear {instance.user.username},\n\nYour withdrawal of ${instance.amount} via {instance.wallet_type} has been received and is pending processing.\n\nThank you."
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], html_message=html_message)

# Signal handler for sending email when withdrawal is verified
@receiver(post_save, sender=Withdrawal)
def send_withdrawal_verified_email(sender, instance, created, **kwargs):
    if not created and instance.status == 'verified':
        # Send email for withdrawal verified
        subject = 'Withdrawal Verified'
        html_message = None
        plain_message = f"Dear {instance.user.username},\n\nYour withdrawal of ${instance.amount} via {instance.wallet_type} has been Verified.\n\nThank you."
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], html_message=html_message)