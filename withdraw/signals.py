from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import WithdrawalsMade

@receiver(post_save, sender=WithdrawalsMade)
def send_withdrawal_verified_email(sender, instance, created, **kwargs):
    if not created and instance.is_verified:
        # Send email for verified withdrawal
        user = instance.user
        subject = 'Withdrawal Request Verified'
        message = f"""
        Dear {user.username},

        Your withdrawal request has been verified and processed successfully.

        Details:
        Wallet: {instance.wallet_type}
        Amount: ${instance.amount}
        Method: {instance.method}

        Best regards,
        Natropi
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
