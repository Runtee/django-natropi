from django.db.models import Sum
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date 
from django.template.loader import render_to_string
from referral.models import Referral
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from accounts.models import CustomUser

User = get_user_model()

@login_required
def update_profile(request):
    print("Inside update_profile view")  

    if request.method == 'POST':
        print("Form submitted via POST")  

        # Get the current user
        profile = request.user

        # Update profile picture
        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        # Update Profile fields
        profile.first_name = request.POST.get('first_name', '')
        profile.last_name = request.POST.get('last_name', '')
        
        # Handle date field
        dob = request.POST.get('dob', '')
        if dob:
            profile.dob = parse_date(dob)
        else:
            profile.dob = None
        
        profile.address1 = request.POST.get('address1', '')
        profile.address2 = request.POST.get('address2', '')
        profile.country = request.POST.get('country', '')
        profile.state = request.POST.get('state', '')
        profile.city = request.POST.get('city', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.bit_wallet = request.POST.get('bit_wallet', '')
        profile.ussdc_wallet = request.POST.get('ussdc_wallet', '')
        profile.paypal_address = request.POST.get('paypal_address', '')
        profile.bank_name = request.POST.get('bank_name', '')
        profile.account_no = request.POST.get('account_no', '')
        profile.bank_address = request.POST.get('bank_address', '')
        profile.sort_code = request.POST.get('sort_code', '')

        # Save the updated profile
        profile.save()

        return redirect('dashboard')  # Redirect to dashboard page after successful update

    # If not a POST request, render the form template
    return render(request, 'user/profile.html')


@login_required
def change_password(request):
    errors = {}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            errors['old_password'] = 'Old password is incorrect.'
        
        if new_password != confirm_password:
            errors['password_mismatch'] = 'New password and confirm password do not match.'
        
        if not errors:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('dashboard')  # Redirect to a success page

    return render(request, 'user/new-password.html', {'errors': errors})