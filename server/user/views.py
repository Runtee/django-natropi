from django.db.models import Sum
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from referral.models import Referral
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm, CustomUserForm, CustomPasswordChangeForm
from .models import Profile
User = get_user_model()
# smail
# Create your views here.


@login_required(login_url='/accounts/login')
def user_dashboard(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)[:5]
    referrals = Referral.objects.filter(user=request.user)
    referrals_profit = referrals.aggregate(
        total_referral_profit=Sum('referral_profit'))['total_referral_profit']

    # profile = Profile.objects.get(user=request.user)
    print(referrals_profit)
    context = {
        'user': user,
        'transactions': transactions,
        'referrals': referrals,
        'referrals_profit': referrals_profit,
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


@login_required
def profile_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = CustomUserForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if profile_form.is_valid() and user_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return render(request, 'user/profile.html')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = CustomUserForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    # For debugging: print the HTML to console
    from django.http import HttpResponse
    html = render_to_string('user/profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form
    })
    print(html)
    return HttpResponse(html)
