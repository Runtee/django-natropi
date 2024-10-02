from typing import Iterable
from django.db import models
from accounts.models import CustomUser as User
from notification.models import Notification
import threading
from utils import send_email

class KYC(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

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
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)    
    verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} KYC"
    
    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:

        if self.pk is not None:
            previous = KYC.objects.get(pk=self.pk)
            # if previous.verified != self.verified:
            if self.status != 'pending':
                status_message = 'verified' if self.verified else 'pending'
                # Create notification
                notification = Notification.objects.create(
                    user=self.user,
                    action='Your KYC status was updated',
                    description=f'Your KYC status has been updated to {self.status}.'
                )
                notification.save()
                email_subject = "Your KYC status was updated"
                email_body = f"Your KYC status has been updated to {self.status}.\n\nThank you for choosing {'Natropi'.capitalize()}.\n\nBest regards,\nThe {'Natropi'.capitalize()} Team"
                email_thread = threading.Thread(target=send_email, args=(email_subject, email_body, self.user.email))
                email_thread.start()
        
        # Call the parent class's save method
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['-submitted_at']
