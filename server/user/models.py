from django.db import models
from accounts.models import CustomUser  

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default.jpg')
    dob = models.DateField(null=True, blank=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    bit_wallet = models.CharField(max_length=100, blank=True, null=True)
    ussdc_wallet = models.CharField(max_length=100, blank=True, null=True)
    paypal_address = models.EmailField(blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=20, blank=True, null=True)
    bank_address = models.CharField(max_length=255, blank=True, null=True)
    sort_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username
