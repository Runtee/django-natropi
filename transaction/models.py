from django.db import models
from accounts.models import CustomUser as User
# Create your models here.

class Transaction(models.Model):
    
    TRANSACTION_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('bonus','Bonus'),
        ('penalty','Penalty'),
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f'{self.user.email} - {self.get_transaction_type_display()}'

