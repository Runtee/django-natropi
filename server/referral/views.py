from django.contrib.auth.decorators import login_required
from .models import Referral
from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
# import threading
# smail

# Create your views here.


@login_required(login_url='/login')
def user_referral(request):

    user = request.user
    referrals = Referral.objects.filter(user=request.user)
    # refdict = {}
    # for c in referrals:
    #     secondref = Profile.objects.get(referred_by=c.user.username)
    #     refdict[c.user.username] = secondref.referral_price

    context = {
        'referrals': referrals,
        'user': user,

    }
    return render(request, 'user/ref.html', context)
