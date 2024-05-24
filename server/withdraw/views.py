from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Withdrawal
from notification.models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
#smail
from website.models import Website
from django.conf import settings

@login_required(login_url='/accounts/login')
def user_withdrawal(request):
    user=request.user
    
    
    withdraws = Withdrawal.objects.filter(user=user).order_by('-created')[:5]

    context = {
        'user': user,
        'withdraws': withdraws,
    }
    website = Website.objects.get(pk=1)
    if request.method == 'POST':
        wallet_address = request.POST.get('wallet_address')
        if not wallet_address:
            messages.info(request, 'You did not add a withdrawal address')
            return redirect('/withdraw')
        
        amount = request.POST.get('amount')
        wallet_type = request.POST.get('wallet_type')
        usdt_amount = request.POST.get('usdt_amount')
        
        if float(usdt_amount) > user.main:
            messages.info(request, 'You have insufficient funds')
            return redirect('/withdraw')
        
        withdraw = Withdrawal.objects.create(user=user, amount=amount, wallet_type=wallet_type, wallet_address=wallet_address, usdt_amount=usdt_amount)
        withdraw.save()
        
        action = f'Your withdrawal of {withdraw.amount} {withdraw.wallet_type} into {withdraw.wallet_address} is pending'
        transaction = Transaction.objects.create(user=user, transaction_type='withdraw', usdt_amount=usdt_amount, description=action)
        transaction.save()
        notification = Notification.objects.create(user=user, action='Withdrawal Pending', description=action)
        notification.save()
        try:
            email_thread = threading.Thread(target=send_email,args=('Withdrawal Requested', f'{user.username} has withdrawn {withdraw.amount} {withdraw.wallet_type} into {withdraw.wallet_address}', settings.RECIPIENT_ADDRESS))
            subject = "Withdrawal Request Pending"
            body = f"Dear {request.user.username},\n\nThis is to inform you that your withdrawal request of {amount} {wallet_type} to {wallet_address} is currently pending processing. Our team will review and complete the withdrawal as soon as possible. If you have any questions or concerns, please do not hesitate to contact our support team.\n\nBest regards,\nThe {(website.name).capitalize()} Team"

            email_thread2 = threading.Thread(target=send_email, args=(subject, body, request.user.email))

            email_thread.start()
            email_thread2.start()
        except Exception as e:
            print(e)
        messages.info(request, 'You have applied for withdrawal')
        return redirect('/withdraw')

    return render(request, 'user/withdraw.html', context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def verify(request,id):
    withdrawal = Withdrawal.objects.get(id=id)
    if withdrawal.verified == False:
        withdrawal.user.main -= int(float(withdrawal.usdt_amount))
        withdrawal.user.save()
        withdrawal.verified = True
        withdrawal.save()
        subject = "Withdrawal Approval Notification"
        body = f"Dear {withdrawal.user.username},\n\nWe are pleased to inform you that your withdrawal request of {withdrawal.amount} {withdrawal.wallet_type} to {withdrawal.wallet_address} has been approved. The funds will be processed accordingly. If you have any questions or need further assistance, please contact our support team.\n\nBest regards,\nThe {(Website.objects.get(pk=1).name).capitalize()} Team"
        email_thread2 = threading.Thread(target=send_email, args=(subject, body, withdrawal.user.email))
        email_thread2.start()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_withdraw(request):
    withdraws = Withdrawal.objects.all()
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'dashboard/withdraw.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_withdraw_completed(request):
    withdraws = Withdrawal.objects.filter(verified=True)
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'dashboard/withdraw2.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_withdraw_pending(request):
    withdraws = Withdrawal.objects.filter(verified=False)
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'dashboard/withdraw3.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def delete_withdraw(request,id):
    withdraw = Withdrawal.objects.get(id=id)
    withdraw.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/accounts/login')
def user_withdraw_completed(request):
    user=request.user
    withdraws = Withdrawal.objects.filter(user=user,verified=True)
    
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'user/completedwithdraw.html',context)

@login_required(login_url='/accounts/login')
def user_withdraw_pending(request):
    user=request.user
    withdraws = Withdrawal.objects.filter(user=user,verified=False)
    
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'user/pendingwithdraw.html',context)
