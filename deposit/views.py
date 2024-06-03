from django.shortcuts import render,redirect
from utils import  can_access_dashboard
# from django.contrib.auth import get_user_model
# User = get_user_model()
from accounts.models import CustomUser as User
from .models import Deposit
# from userprofile.decorators import check_profile_exists
from walletaddress.models import WalletAddress, Acct
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
from website.models import Website
from django.conf import settings
from notification.models import Notification
# Create your views here.


@login_required(login_url='/login')
def user_deposit(request):
    user = request.user
    deposits = Deposit.objects.filter(user=user).order_by('-created')[:5]
    
    context = {
        'deposits': deposits,
        'user':user, 
    }
 
    return render(request,'user/deposit.html',context)

@login_required(login_url='/login')
def user_deposit_form(request):
    user = request.user
    numacc = Acct.objects.filter(status="1")
    # form = DepositForm()
    context = {"numacc":numacc}
    #'amount', 'method', 'address', 'trans_hash'
    if request.method == 'POST':
        wallet_address = request.POST['address']
        amount = request.POST['amount']
        usdt_amount = request.POST['amount']
        wallet_type = request.POST['method']
        trans_hash = request.POST['trans_hash']
        
        print(wallet_type)
        deposit = Deposit.objects.create(user=user,amount=amount,wallet_type=wallet_type,wallet_address=wallet_address,usdt_amount=usdt_amount)
        deposit.save()
        print(deposit.wallet_type)
        action = f'Your deposit of {deposit.amount} {deposit.wallet_type} into {deposit.wallet_address} is pending'
        notification = Notification.objects.create(user=user, action='Deposit Pending', description=action)
        notification.save()
        transaction = Transaction.objects.create(user=user, transaction_type='deposit', usdt_amount=usdt_amount, description=action)
        transaction.save()
        website = Website.objects.get(pk=1)
        try:
            email_thread = threading.Thread(target=send_email,args=('Deposit Requested',f'{user.username} has deposited {deposit.amount} {deposit.wallet_type} into {deposit.wallet_address}', settings.RECIPIENT_ADDRESS)        )
            email_subject = "Deposit Requested"
            email_body = f"Dear {request.user.username},\n\nWe acknowledge your deposit request of {amount} {wallet_type} into the wallet address {wallet_address}. Please note that your request is currently pending processing. Our team will review and complete the deposit as soon as possible.\n\nThank you for choosing {(website.name).capitalize()}.\n\nBest regards,\nThe {(website.name).capitalize()} Team"
            email_thread2 = threading.Thread(target=send_email, args=(email_subject, email_body, request.user.email))
            email_thread.start()
            email_thread2.start()
        except Exception as e:
            print(e)
        messages.info(request, 'You have applied for a deposit')
        return redirect('/deposit')
        
    return render(request,'user/deposit_form.html',context)

def verify(request,id):
    deposit = Deposit.objects.get(id=id)
    if deposit.verified == False:
        deposit.verified = True
        deposit.save()
        try:
            email_thread2 = threading.Thread(target=send_email,args=('Deposit Approved', f'Your deposit of {deposit.amount} {deposit.wallet_type} into {deposit.wallet_address} has been', deposit.user.email))
            email_thread2.start()
        except Exception as e:
            print(e)
    return redirect(request.META.get('HTTP_REFERER', '/admin'))

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_deposit(request):
    deposits = Deposit.objects.all()
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_deposit_completed(request):
    deposits = Deposit.objects.filter(verified=True)
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit3.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_deposit_pending(request):
    deposits = Deposit.objects.filter(verified=False)
    
    context = {
        'deposits':deposits,
    }
    return render(request,'dashboard/deposit4.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def delete_deposit(request,id):
    deposit = Deposit.objects.get(id=id)
    deposit.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login')
def user_deposit_completed(request):
    user=request.user
    deposits = Deposit.objects.filter(user=user,verified=True)
    
    
    context = {
        'deposits':deposits,
    }
    return render(request,'user/completeddeposit.html',context)

@login_required(login_url='/login')

def user_deposit_pending(request):
    user = request.user
    deposits = Deposit.objects.filter(user=user,verified=False)
    
    
    context = {
        'deposits':deposits,
    }
    return render(request,'user/pendingdeposit.html',context)
