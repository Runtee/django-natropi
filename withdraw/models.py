from django.db import models
from accounts.models import CustomUser
import threading
from utils import send_email

# Create your models here.    

class WithdrawalsMade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wallet_type = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    message = models.CharField(max_length=255, null=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_verified == True:
            # self.user.main -=  float(self.amount)
            action = f'Your withdraw of {self.amount} {self.wallet_type} is verified'
            self.user.notification_set.create(user=self.user,action='Verified',description=f'Your withdraw of {self.amount} {self.wallet_type} has been verified')
            self.user.transaction_set.create(user=self.user, transaction_type='deposit', usdt_amount=self.amount, description=action,verified=True)
            self.user.save()
            try:
                email_thread = threading.Thread(target=send_email,args=('Withdrawal Verified',f'Your withdraw of {self.amount} {self.wallet_type} is verified',self.user.email))
                email_thread.start()
            except Exception as e:
                print(e)
            
             
        return super().save(*args, **kwargs)
  

    @property
    def status(self):
        return "verified" if self.is_verified else "pending"

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
    
    
