from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from .models import WithdrawalsMade
from django.conf import settings



@login_required(login_url='/login')
def withdraw_view(request):
    user = request.user
    errors = {}

    if request.method == "POST":
        wallet = request.POST.get('wallet')
        method = request.POST.get('method')

        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            errors['amount'] = 'Invalid amount entered.'
            return render(request, 'user/withdraw_form.html', {
                'user': user,
                'errors': errors,
            })

        if method == "bit_wallet" and (not user.bit_wallet or user.bit_wallet.strip() in ['', 'None']):
            errors['method'] = 'Bitcoin wallet address does not exist.'
            return render(request, 'user/withdraw_form.html', {'errors': errors})
        elif method == "ussdc_wallet" and (not user.ussdc_wallet or user.ussdc_wallet.strip() in ['', 'None']):
            errors['method'] = 'USSD wallet address does not exist.'
            return render(request, 'user/withdraw_form.html', {'errors': errors})
        elif method == "bank" and (not (user.bank_name and user.account_no) or user.bank_name.strip() in ['', 'None'] or user.account_no.strip() in ['', 'None']):
            errors['method'] = 'Bank details do not exist.'
            return render(request, 'user/withdraw_form.html', {'errors': errors})
        elif method not in ["bit_wallet", "ussdc_wallet", "bank"]:
            errors['method'] = 'Invalid withdrawal method selected.'
            return render(request, 'user/withdraw_form.html', {'errors': errors})
        if not errors:
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

                messages.success(request, 'Withdrawal request sent. Withdrawal is pending.')

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
            else:
                errors['balance'] = f"Amount greater than {wallet} balance."

    withdrawals = WithdrawalsMade.objects.filter(user=user).order_by('-date')

    return render(request, 'user/withdraw.html', {
        'user': user,
        'errors': errors,
        'withdrawals': withdrawals,
    })

def withdrawal(request):
    return render(request, 'user/withdraw.html')


def withdrawal_form(request):
    return render(request, 'user/withdraw_form.html')
