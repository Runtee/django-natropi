from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import KYCForm
from .models import KYC

@login_required
def submit_kyc(request):
    try:
        kyc = KYC.objects.get(user=request.user)
        form = KYCForm(instance=kyc)
    except KYC.DoesNotExist:
        form = KYCForm()

    if request.method == 'POST':
        if kyc:
            form = KYCForm(request.POST, request.FILES, instance=kyc)
        else:
            form = KYCForm(request.POST, request.FILES)

        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.save()
            messages.success(request, 'KYC submitted successfully.')
            return redirect('kyc_status')

    return render(request, 'user/kyc.html', {'form': form})

@login_required
def kyc_status(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None

    return render(request, 'user/kyc_status.html', {'kyc': kyc})
