from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
from accounts.models import CustomUser
from .models import Transfer, P2PTransfer

@login_required
def transfer_view(request):
    user = request.user
    errors = {}

    if request.method == "POST":
        from_wallet = request.POST.get('from_wallet')
        to_wallet = request.POST.get('to_wallet')
        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            errors['amount'] = 'Invalid amount entered.'
            return render(request, 'user/transfer.html', {'errors': errors})

        # Ensure wallets are different
        if from_wallet == to_wallet:
            errors['wallet'] = 'Source and destination wallets must be different.'
            return render(request, 'user/transfer.html', {'errors': errors})

        from_balance = getattr(user, from_wallet, Decimal('0.00'))
        to_balance = getattr(user, to_wallet, Decimal('0.00'))

        if from_balance >= amount:
            setattr(user, from_wallet, from_balance - amount)
            setattr(user, to_wallet, to_balance + amount)
            user.save()

            # Save transfer record
            Transfer.objects.create(
                user=user,
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount
            )

            messages.success(request, 'Transfer successful.')
            return redirect('transfers')
        else:
            errors['balance'] = f"Insufficient balance in {from_wallet}."

    # Fetch transfer records
    transfers = Transfer.objects.filter(user=user).order_by('-date')

    return render(request, 'user/transfer.html', {'user': user, 'errors': errors, 'transfers': transfers})


@login_required
def p2p_transfer_view(request):
    user = request.user
    errors = {}

    if request.method == "POST":
        recipient_email = request.POST.get('recipient_email')
        try:
            recipient = CustomUser.objects.get(email=recipient_email)
        except CustomUser.DoesNotExist:
            errors['recipient_email'] = 'Recipient email does not exist.'
            return render(request, 'user/p2p-form.html', {'errors': errors})

        from_wallet = 'main'
        to_wallet = 'main'

        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            errors['amount'] = 'Invalid amount entered.'
            return render(request, 'user/p2p-form.html', {'errors': errors})

        if amount <= 0:
            errors['amount'] = 'Amount must be greater than zero.'
            return render(request, 'user/p2p-form.html', {'errors': errors})

        from_balance = getattr(user, from_wallet, Decimal('0.00'))

        if from_balance >= amount:
            setattr(user, from_wallet, from_balance - amount)
            setattr(recipient, to_wallet, getattr(recipient, to_wallet, Decimal('0.00')) + amount)
            user.save()
            recipient.save()

            # Save transfer record
            P2PTransfer.objects.create(
                user=user,
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
                recipient_email=recipient_email
            )

            messages.success(request, 'Transfer successful.')

        # Send email notification
            subject = 'Transfer Successful'
            plain_message = f"Dear {user.username},\n\nYour transfer of ${amount} from {from_wallet} wallet to {recipient_email} has is successful. \n\nThank you."
            html_message = None

            send_mail(
                subject,
                strip_tags(plain_message),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                )

            return redirect('transfer_success')
        else:
            errors['balance'] = 'Insufficient balance in the main wallet.'
            
    transfers = P2PTransfer.objects.filter(user=user).order_by('-date')

    return render(request, 'user/p2p.html', {'user': user, 'errors': errors, 'transfers': transfers})

@login_required
def transfer(request):
    return render(request, 'user/transfer.html')

@login_required
def transfer_form(request):
    return render(request, 'user/transfer_form.html')

def p2p(request):
    return render(request, 'user/p2p.html')

def p2p_form(request):
    return render(request, 'user/p2p-form.html')