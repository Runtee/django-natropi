import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import *
from .models import CustomUser
from django.urls import reverse, reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.db.models import F
from referral.models import Referral
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from decimal import Decimal
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)



User = get_user_model()


def register(request):
    referral_code = request.GET.get('referral_code', '')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()

            # Get the current site
            current_site = get_current_site(request)

            referral_code = form.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    referrer_user = User.objects.get(referrals__referral_code=referral_code)
                    referral = Referral.objects.create(
                        referrer=referrer_user,
                        referred_user=user,
                        referral_code=str(uuid.uuid4())[:10]
                    )

                    # Update referrer's referral count and bonus
                    referrer_user.referrals.update(referral_count=F('referral_count') + 1)
                    referrer_user.referrals.update(referral_bonus=F('referral_bonus') + Decimal('10.00'))
                    referrer_user.main += Decimal('1.00')
                    referrer_user.save()
                    messages.success(request, 'You have been registered successfully and the referrer has been rewarded.')

                    # Send email notification to referrer
                    subject = 'Referral Successful'
                    plain_message = f"Dear {referrer_user.username},\n\nSomeone has registered using your referral code. You have received a bonus of 10 units and $1 has been added to your main balance.\n\nThank you."
                    html_message = None

                    send_mail(
                        subject,
                        strip_tags(plain_message),
                        settings.DEFAULT_FROM_EMAIL,
                        [referrer_user.email],
                        html_message=html_message,
                    )
                except User.DoesNotExist:
                    messages.error(request, "Referral code is invalid.")
                    return render(request, 'register.html', {'form': form})

            # Automatically create a Referral object for the new user
            Referral.objects.create(
                referrer=user,
                referral_code=str(uuid.uuid4())[:10]
            )

            # Create email subject and message
            mail_subject = 'Activate your account'
            token = default_token_generator.make_token(user)
            html_message = render_to_string('other/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = form.cleaned_data.get('email')

            # Send the email
            email = EmailMultiAlternatives(mail_subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, 'Verification email sent. Please check your inbox.')

            return render(request, 'other/verification_sent.html')
        else:
            # If the form is not valid, add an error message
            messages.error(request, 'There was an error with your registration. Please check the details and try again.')
    else:
        form = RegistrationForm(initial={'referral_code': referral_code})

    return render(request, 'register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        login(request, user)
        return render(request, 'other/activation_successful.html')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
    

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('other/verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
    email.attach_alternative(message, "text/html")
    email.send()


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.email_verified:
                    login(request, user)
                    return redirect("/user")
                else:
                    # Resend activation email
                    send_activation_email(user, request)
                    messages.error(request, 'Your account is not activated. We have resent the activation email. Please check your inbox.')
                    return render(request, 'login.html', {'form': form})
            else:
                form.add_error(None, 'Invalid email or password')
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context)

def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email, is_active=True)
            for user in users:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                subject = 'Password Reset Request'
                html_message = render_to_string('other/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                plain_message = strip_tags(html_message)  # Generate plain text message
                from_email = settings.DEFAULT_FROM_EMAIL

                # Create email message
                email_message = EmailMultiAlternatives(subject, plain_message, from_email, [email])
                email_message.attach_alternative(html_message, "text/html")
                email_message.send()

            return render(request, 'other/password_reset_done.html') 
        else:
            print(form.errors)
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot-password.html', {'form': form})

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'other/password_reset_done.html'


def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been set. You may go ahead and log in now.')
                return render(request, 'other/password_reset_complete.html')
        else:
            form = CustomSetPasswordForm(user)
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        form = None

    return render(request, 'other/password_reset_confirm.html', {'form': form})

