from django.db import models
from userprofile.models import Profile

# Create your models here.
class Transfer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transfers_made')
    transfer_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transfers_received')
    created = models.DateTimeField(auto_now_add=True)
    usdt_amount = models.DecimalField(max_digits=20,decimal_places=5,blank=True,null=True)
    transferred = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'{self.profile.user.get_username()} transferred {self.usdt_amount} to {self.transfer_profile.user.get_username()}'
        
    
