from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Referral
from userprofile.decorators import check_profile_exists
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
# import threading
from utils import send_email
#smail
from django.conf import settings

# Create your views here.
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_referral(request):
    
    
    profile = Profile.objects.get(user=request.user)
    referrals = Referral.objects.filter(user=request.user)
    # refdict = {}
    # for c in referrals:
    #     secondref = Profile.objects.get(referred_by=c.user.username)
    #     refdict[c.user.username] = secondref.referral_price
    
    context = {
 
        'referrals':referrals,
        'profile':profile,
      
    }
    return render(request,'user/ref.html',context)
