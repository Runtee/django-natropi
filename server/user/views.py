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

@login_required(login_url='/login')
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
        messages.success(request,"update successful")
        return redirect('profile')  # Redirect to dashboard page after successful update

    # If not a POST request, render the form template
    return render(request, 'user/profile.html')


@login_required(login_url='/login')
def change_password(request):

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request,'Old password is incorrect.')
            return render(request, 'user/new-password.html',)
        
        if new_password != confirm_password:
            messages.error(request,'New password and confirm password do not match.')
            return render(request, 'user/new-password.html',)
        
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
        messages.success(request, 'Your password has been updated successfully.')
        return redirect('profile')  # Redirect to a success page

    return render(request, 'user/new-password.html',)

@login_required(login_url='/login')
def user_dashboard(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'user/index.html', context)


def my_custom_error_view(request):
    return render(request, 'other/error.html')

def my_custom_page_not_found_view(request, exception):
    return render(request, 'other/error.html')

def my_custom_bad_request_view(request, exception):
    return render(request, 'other/error.html')

def my_custom_permission_denied_view(request, exception):
    return render(request, 'other/error.html')