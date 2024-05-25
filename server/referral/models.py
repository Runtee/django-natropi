from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Referral (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    referred_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='referred_user')
    referral_profit = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def __str__(self):
        return f'{self.user} referred {self.referred_user}'