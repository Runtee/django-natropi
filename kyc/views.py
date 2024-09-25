from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import KYCForm
from .models import KYC

@login_required
def submit_kyc(request):
    kyc = None 
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
            kyc.status = 'pending'  # When a user submits, status is set to "Pending"
            kyc.rejection_reason = ''
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


@login_required
def admin_review_kyc(request, kyc_id):
    kyc = KYC.objects.get(id=kyc_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            kyc.status = 'approved'
            kyc.rejection_reason = None  # Clear rejection reason
            messages.success(request, 'KYC approved successfully.')
        elif 'reject' in request.POST:
            kyc.status = 'rejected'
            kyc.rejection_reason = request.POST.get('rejection_reason', 'No reason provided.')
            messages.error(request, 'KYC rejected with reason: ' + kyc.rejection_reason)
        
        kyc.save()
        return redirect('admin_kyc_review')

    return render(request, 'admin/review_kyc.html', {'kyc': kyc})