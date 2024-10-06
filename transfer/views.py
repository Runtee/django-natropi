from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from decimal import Decimal
from accounts.models import CustomUser
from .models import Transfer, P2PTransfer


@login_required(login_url='/login')
def transfer_view(request):
    user = request.user

    if request.method == "POST":
        from_wallet = request.POST.get('from_wallet')
        to_wallet = request.POST.get('to_wallet')
        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            messages.error(request, 'Invalid amount entered.')
            return render(request, 'user/transfer_form.html',)

        # Ensure wallets are different
        if from_wallet == to_wallet:
            messages.error(
                request, 'Source and destination wallets must be different.')
            return render(request, 'user/transfer_form.html')

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
            return redirect('/transfer')
        else:
            messages.error(request, f"Insufficient balance in {from_wallet}.")
            return render(request, 'user/transfer_form.html')

    return render(request, 'user/transfer_form.html', {'user': user})


@login_required
def transfer(request):
    user = request.user
    transfers = Transfer.objects.filter(user=user).order_by('-date')
    context = {
        "user": user,
        "transfers": transfers
    }
    return render(request, 'user/transfer.html', context)


@login_required(login_url='/login')
def p2p(request):
    user = request.user

    transfers = P2PTransfer.objects.filter(
        Q(user=user) | Q(recipient_email__icontains=user.email)

    ).order_by('-date')

    return render(request, 'user/p2p.html', {"transfers":transfers})


@login_required(login_url='/login')
def p2p_transfer_view(request):
    user = request.user


    if request.method == "POST":
        recipient_email = request.POST.get('recipient_email')
        try:
            recipient = CustomUser.objects.get(email__icontains=recipient_email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Recipient email does not exist.')
            return render(request, 'user/p2p-form.html')

        from_wallet = 'main'
        to_wallet = 'main'

        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            messages.error(request, 'Invalid amount entered.')
            return render(request, 'user/p2p-form.html')

        if amount <= 0:
            messages.error(request, 'Amount must be greater than zero.')
            return render(request, 'user/p2p-form.html',)

        from_balance = getattr(user, from_wallet, Decimal('0.00'))

        if from_balance >= amount:
            setattr(user, from_wallet, from_balance - amount)
            setattr(recipient, to_wallet, getattr(
                recipient, to_wallet, Decimal('0.00')) + amount)
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
            plain_message = f"Dear {user.username},\n\nYour transfer of ${amount} from {from_wallet} wallet to {recipient_email} is successful. \n\nThank you."
            html_message = None

            send_mail(
                subject,
                strip_tags(plain_message),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
            )

            # Send email notification to the recipient
            subject_recipient = 'Funds Received'
            plain_message_recipient = f"Dear {recipient.username},\n\nYou have received ${amount} in your {to_wallet} wallet from {user.email}.\n\nThank you."
            send_mail(
                subject_recipient,
                plain_message_recipient,
                settings.DEFAULT_FROM_EMAIL,
                [recipient.email],
            )

            return redirect('p2p')
        else:
            messages.error(request, 'Insufficient balance in the main wallet.')

    return render(request, 'user/p2p-form.html', {'user': user, })

