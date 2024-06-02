from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def user_referrals(request):
    # Fetch referral data
    referrals = request.user.users_user.all()

    for referral in referrals:
        print(f"Referral: {referral.username}, Image: {referral.image.url}")

    # Render the referrals template
    return render(request, 'user/referrals.html', {'referrals': referrals})
