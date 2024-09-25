from .models import WithdrawalsMade
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import threading
from utils.util import send_email
User = get_user_model()


@login_required(login_url='/login')
def withdraw_view(request):
    user = request.user

    if request.method == "POST":
        wallet = request.POST.get('wallet')
        method = request.POST.get('method')

        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            messages.error(request,'Invalid amount entered.')
            return render(request, 'user/withdraw_form.html', {
                'user': user,
            })

        if method == "bit_wallet" and (not user.bit_wallet or user.bit_wallet.strip() in ['', 'None']):
            messages.error(request,'Bitcoin wallet address does not exist.')
            return render(request, 'user/withdraw_form.html')
        elif method == "ussdc_wallet" and (not user.ussdc_wallet or user.ussdc_wallet.strip() in ['', 'None']):
            messages.error(request,'USSD wallet address does not exist.')
            return render(request, 'user/withdraw_form.html')
        elif method == "bank" and (not (user.bank_name and user.account_no) or user.bank_name.strip() in ['', 'None'] or user.account_no.strip() in ['', 'None']):
            messages('Bank details do not exist.')
            return render(request, 'user/withdraw_form.html')
        elif method not in ["bit_wallet", "ussdc_wallet", "bank"]:
            messages.error(request,'Invalid withdrawal method selected.')
            return render(request, 'user/withdraw_form.html')
        
        current_balance = getattr(user, wallet, Decimal('0.00'))
        if current_balance >= amount:
            setattr(user, wallet, current_balance - amount)
            user.save()
            withdrawal = WithdrawalsMade.objects.create(
                user=user,
                wallet_type=wallet,
                amount=amount,
                method=method,
                message=f"Withdraw Fund via {wallet.capitalize()} Wallet"
            )
            messages.success(
                request, 'Withdrawal request sent. Withdrawal is pending.')
            # Send email notification
            subject = 'Withdrawal Request Received'
            plain_message = f"Dear {user.username},\n\nYour withdrawal of ${withdrawal.amount} via {withdrawal.wallet_type} Wallet has been received and is pending processing.\n\nThank you."
            html_message = None
            send_mail(
                subject,
                strip_tags(plain_message),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )
            redirect('withdraw')
        else:
            messages.error(request,f"Amount greater than {wallet} balance.")
            return render(request, 'user/withdraw_form.html')
    return render(request, 'user/withdraw_form.html')


@login_required(login_url='/login')
def withdrawal(request):
    user = request.user
    withdrawals = WithdrawalsMade.objects.filter(user=user).order_by('-date')

    return render(request, 'user/withdraw.html', {'withdrawals': withdrawals, })

def verify(request,id):
    withdrawal = WithdrawalsMade.objects.get(id=id)
    if withdrawal.is_verified == False:
        withdrawal.is_verified = True
        withdrawal.save()
        try:
            email_thread2 = threading.Thread(target=send_email,args=('Withdrawal Approved', f'Your withdrawal of {withdrawal.amount} {withdrawal.wallet_type} has been verified', withdrawal.user.email))
            email_thread2.start()
        except Exception as e:
            print(e)
    return redirect(request.META.get('HTTP_REFERER', '/admin'))
