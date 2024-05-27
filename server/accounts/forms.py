from django import forms
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms



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


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'type': 'email',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email, is_active=True).count() == 0:
            raise forms.ValidationError("There is no user registered with the specified email address.")
        return email


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
