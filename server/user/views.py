from django.db.models import Sum
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from referral.models import Referral
from django.shortcuts import render
from django.contrib.auth import get_user_model
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
