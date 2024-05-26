from django import forms
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django_countries.fields import CountryField
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control account',
        'placeholder': 'Confirm Password'
    }))
    referral_code = forms.CharField(widget= forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Referral Code'
            }), required=False)
    terms = forms.BooleanField()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'country', 'phone', 'password',]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Last Name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Email Address',
                'maxlength': '320',
                'required': True,
                'id': 'id_email'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Phone'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control account',
                'placeholder': 'Password'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control account',
        'placeholder': 'Email Address',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'cb-remember',
    }))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control account',
            'placeholder': 'Email Address',
            'type': 'email',
        })
    )

    def save(self, domain_override=None,
             subject_template_name='password_reset_subject.txt',
             email_template_name='password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):

        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            subject = render_to_string(subject_template_name, context)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            body = render_to_string(email_template_name, context)
            send_mail(subject, body, from_email, [user.email], html_message=html_email_template_name and render_to_string(html_email_template_name, context))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'type': 'password',
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'type': 'password',
        }),
    )
