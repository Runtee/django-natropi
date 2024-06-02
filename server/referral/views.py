from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Referral

@login_required
def user_referrals(request):
    user = request.user
    user_referral = Referral.objects.filter(referrer=user).first()
    referred_users = Referral.objects.filter(referrer=user, referred_user__isnull=False)

    context = {
        'user': user,
        'user_referral': user_referral,
        'referrals': referred_users,
        'referral_count': referred_users.count(),
    }
    return render(request, 'user/referrals.html', context)
