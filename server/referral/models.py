from django.db import models
from django.conf import settings

class Referral(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referred_by', null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referral_count = models.IntegerField(default=0)
    referral_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Referral by {self.referrer.username}"
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:10]
        super().save(*args, **kwargs)
