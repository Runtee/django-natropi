from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Transfer

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
