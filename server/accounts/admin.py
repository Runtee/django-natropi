from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new custom users. Includes all the required fields, plus a repeated password field."""
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def save(self, commit=True):
        # Hash the password before saving
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """A form for updating existing custom users. Includes all fields but makes password read-only."""

    class Meta:
        model = CustomUser
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'readonly': 'readonly'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the password field is read-only
        self.fields['password'].disabled = True

    def clean_password(self):
        # Return the initial value of the password, ensuring it is not changed
        return self.initial["password"]
    
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Customize the fields displayed in the admin list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active')

    # Customize the fields displayed in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': (
            'username', 'first_name', 'last_name', 'country', 'phone', 'dob', 'image', 'referral', 'referral_code', 'referral_count', 'referral_bonus')}),
        (_('Location'), {'fields': ('address1', 'address2', 'city', 'state')}),
        (_('Wallets'), {'fields': ('bit_wallet', 'ussdc_wallet', 'paypal_address',
         'bank_name', 'account_no', 'bank_address', 'sort_code')}),
        (_('Balances'), {
         'fields': ('main', 'portfolio', 'strategy', 'trade')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
