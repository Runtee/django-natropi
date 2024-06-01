from django.db import models
from accounts.models import CustomUser

# Create your models here.    

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
    
    
