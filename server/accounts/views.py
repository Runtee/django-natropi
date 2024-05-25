import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import *
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
                    pass 

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
            print('Verification sent')

            return render(request, 'verification_sent.html')
            

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


class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot-password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'