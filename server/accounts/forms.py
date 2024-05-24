from django import forms
from .models import CustomUser
from django_countries.fields import CountryField

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    country = CountryField(blank_label='(select country)').formfield()
    phone_number = forms.CharField(max_length=15)
    terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms and conditions to register'})


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password


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