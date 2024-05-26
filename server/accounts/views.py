from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.urls import reverse_lazy
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
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib import messages


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
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
            message = render_to_string('verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user.verification_token,
            })
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = form.cleaned_data.get('email')

            # Send the email
            send_mail(mail_subject, message, from_email, [to_email])
            messages.success(request, 'Verification email sent. Please check your inbox.')

            return render(request, 'verification_sent.html')
        else:
            # If the form is not valid, add an error message
            messages.error(request, 'There was an error with your registration. Please check the details and try again.')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


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
