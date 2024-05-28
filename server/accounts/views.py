import uuid
from django.shortcuts import render, redirect
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
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from referral.models import Referral
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)



User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email is verified
            user.verification_token = str(uuid.uuid4())  # Generate a unique token
            user.save()

            # Get the current site
            current_site = get_current_site(request)

            referral_code = form.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    referred_by = CustomUser.objects.get(referral__referral_code=referral_code)
                    Referral.objects.create(user=referred_by, referred_user=user)
                except CustomUser.DoesNotExist:
                    messages.error(request, "Referral code is invalid.")
                    return render(request, 'register.html', {'form': form})

            # Create email subject and message
            mail_subject = 'Activate your account'
            html_message = render_to_string('other/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.verification_token,
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
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'register.html')


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                form.add_error(None, 'Invalid email or password')

    context = {
        'form': form,
    }
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
                message = render_to_string('other/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                print(subject, message,settings.DEFAULT_FROM_EMAIL, [email])
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            return render(request, 'other/password_reset_done.html') 
        else:
            print(form.errors)
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot-password.html', {'form': form})

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'other/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'other/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'other/password_reset_complete.html'