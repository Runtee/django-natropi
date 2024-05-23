from django.db import models
from userprofile.models import Profile
# Create your models here.

class Transaction(models.Model):
    
    TRANSACTION_CHOICES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('bonus','Bonus'),
        ('penalty','Penalty'),
    )
    
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return f'{self.profile.user.username} - {self.get_transaction_type_display()}'

