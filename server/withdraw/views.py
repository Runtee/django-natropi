from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from .models import Withdrawal
from decimal import Decimal
from notification.models import Notification
from django.contrib import messages
from user.models import Profile
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
#smail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from website.models import Website
from .models import Account, WithdrawalsMade
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
    return render(request,'user/withdraw.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_withdraw_completed(request):
    withdraws = Withdrawal.objects.filter(verified=True)
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'user/withdraw2.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_withdraw_pending(request):
    withdraws = Withdrawal.objects.filter(verified=False)
    
    context = {
        'withdraws':withdraws,
    }
    return render(request,'user/withdraw3.html',context)

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


@login_required
def withdraw_view(request):
    user = request.user
    user_profile = user.profile
    user_account = Account.objects.get(user=user)
    errors = {}

    if request.method == "POST":
        wallet = request.POST.get('wallet')
        method = request.POST.get('method')

        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            errors['amount'] = 'Invalid amount entered.'
            return render(request, 'user/withdraw.html', {
                'profile': user_profile,
                'account': user_account,
                'errors': errors,
            })

        if method == "bit_wallet":
            if not user_profile.bit_wallet:
                errors['method'] = 'Bitcoin wallet does not exist.'
        elif method == "ussdc_wallet":
            if not user_profile.ussdc_wallet:
                errors['method'] = 'USSD wallet does not exist.'
        elif method == "bank":
            if not (user_profile.bank_name and user_profile.account_no):
                errors['method'] = 'Bank details do not exist.'
        else:
            errors['method'] = 'Invalid withdrawal method selected.'

        if not errors:
            wallet_balance_field = f"{wallet}_balance"
            current_balance = getattr(user_account, wallet_balance_field, Decimal('0.00'))

            if current_balance >= amount:
                setattr(user_account, wallet_balance_field, current_balance - amount)
                user_account.save()

                withdrawal = WithdrawalsMade.objects.create(
                    user=user,
                    wallet_type=wallet,
                    amount=amount,
                    method=method,
                    message=f"Withdraw Fund via {wallet.capitalize()} Wallet"
                )

                messages.success(request, 'Withdrawal request sent. Withdrawal is pending.')

                # Send email notification
                subject = 'Withdrawal Request Received'
                context = {'withdrawal': withdrawal}
                plain_message = f"Dear {user.username},\n\nYour withdrawal of ${withdrawal.amount} via {withdrawal.wallet_type} Wallet has been received and is pending processing.\n\nThank you." 
                html_message = None

                send_mail(
                    subject,
                    strip_tags(plain_message),
                    settings.DEFAULT_FROM_EMAIL,  # Replace with your email
                    [user.email],
                    html_message=html_message,
                )
            else:
                errors['balance'] = f"Amount greater than {wallet} balance."

    withdrawals = WithdrawalsMade.objects.filter(user=user).order_by('-date')

    return render(request, 'user/withdraw.html', {
        'profile': user_profile,
        'account': user_account,
        'errors': errors,
        'withdrawals': withdrawals,
    })