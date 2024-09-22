from django.db import models
from accounts.models import CustomUser as User

class KYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100, choices=[
        ('passport', 'Passport'),
        ('driver_license', 'Driver’s License'),
        ('national_id', 'National ID Card'),
    ])
    document_number = models.CharField(max_length=50)
    document_image = models.ImageField(upload_to='kyc_documents/')
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)    
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} KYC"

    class Meta:
        ordering = ['-submitted_at']  # Order by submission date, newest first
