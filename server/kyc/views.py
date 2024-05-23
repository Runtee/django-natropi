from django.shortcuts import render,redirect
from utils import  can_access_dashboard, send_email
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Kyc
from userprofile.decorators import check_profile_exists
from notification.models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
from .forms import KycForm
import threading
# Create your views here.
#make and readonly and do like deposit verify
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_kyc(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        kyc = Kyc.objects.get(profile=profile)
        verified = kyc.verified
    except (Profile.DoesNotExist, Kyc.DoesNotExist):
        kyc = None
        verified = False

    if request.method == 'POST':
        form = KycForm(request.POST, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.profile = profile
            kyc.save()
            notification = Notification.objects.create(profile=profile, action='Kyc Submitted', description='You have successfully submitted your Kyc form')
            notification.save()
            messages.success(request, 'You have successfully submitted your KYC form.')
            return redirect('/kyc')
    else:
        form = KycForm(instance=kyc)

    context = {
        'verified': verified,
        'profile': profile,
        'form': form,
        'kyc': bool(kyc)
    }
    print(bool(kyc))
    return render(request, 'user/kyc.html', context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def verify(request,id):
    profile = Profile.objects.get(user=request.user)
    kyc = Kyc.objects.get(id=id)
    if kyc.verified == False:
        kyc.verified = True
        kyc.save()
        notification = Notification.objects.create(profile=profile, action='Kyc Verified', description=f'Your Kyc form was verified')
        notification.save()
        threading.Thread(target=send_email,args=('Kyc Verified', f'Your Kyc form was verified', request.user.email))
    return redirect(request.META.get('HTTP_REFERER', '/'))