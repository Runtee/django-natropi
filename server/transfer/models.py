from django.db import models
from accounts.models import CustomUser as User

# Create your models here.
class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers_made')
    transfer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers_received')
    created = models.DateTimeField(auto_now_add=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    transferred = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'{self.user.email} transferred {self.usdt_amount} to {self.transfer_user.user.email}'
        
    
