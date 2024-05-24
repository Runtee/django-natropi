from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from .models import Transfer
from walletaddress.models import WalletAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
import threading
from utils import send_email
from website.models import Website
from accounts.models import CustomUser as User
#smail
from django.conf import settings
# Create your views here.
from django.db import transaction

@login_required(login_url='/accounts/login')
# @check_profile_exists
@transaction.atomic
def user_transfer(request):
    if request.method == 'POST':
        try:
            email_address = request.POST.get('wallet_address')
            amount = float(request.POST.get('amount'))
            wallet_type = request.POST.get('wallet_type')
            usdt_amount = float(request.POST.get('usdt_amount'))
            
            user = request.user
            
            if usdt_amount > user.main:
                messages.error(request, 'You have insufficient funds')
                return redirect('/transfer')
            
            try:
                transfer_user = User.objects.get(email=email_address)
            except Exception as e:
                print(e)
                messages.error(request, 'There was an error with the user')
                return redirect('/transfer')
            
            with transaction.atomic():
                transfer = Transfer.objects.create(user=user,transfer_user=transfer_user, usdt_amount=usdt_amount)
                transfer_user = Transfer.objects.create(user=user,transfer_user=transfer_user, usdt_amount=usdt_amount, transferred=False)
                
                user.main -= usdt_amount
                user.save()
                transfer_user.main += usdt_amount
                transfer_user.save()
                
                Transaction.objects.create(user=user, transaction_type='transfer', usdt_amount=usdt_amount, description=f'You have transferred {usdt_amount} {wallet_type} to {transfer_user.user.username}')
                Transaction.objects.create(user=transfer_user, transaction_type='transfer', usdt_amount=usdt_amount, description=f'{user.username} has transferred {usdt_amount} {wallet_type} to you')
                
                # Assuming you have a function send_email_task
                website = Website.objects.get(pk=1)
                try:
                    subject = "Transfer Confirmation"
                    body = f"Dear {user.username},\n\nThis is to confirm that you have successfully transferred {transfer.usdt_amount} usd to the recipient with the email address {transfer_user.email}. If you have any questions or concerns about this transaction, please do not hesitate to contact our support team.\n\nBest regards,\nThe {(website.name).capitalize()} Team"

                    email_thread = threading.Thread(target=send_email, args=(subject, body, user.email))
                    email_thread.start()

                    email_thread2 = threading.Thread(target=send_email,args=('Transfer', f'{user.username} has transferred {transfer.usdt_amount} usd to {transfer_user.email}', settings.RECIPIENT_ADDRESS))
                    email_thread2.start()
                    subject1 = "Incoming Transfer Notification"
                    body1 = f"Dear {transfer_user.username},\n\nWe are pleased to inform you that {user.username} has successfully transferred {transfer.usdt_amount} usd to your account. If you have any questions or need assistance, feel free to reach out. Thank you for choosing {(website.name).capitalize()}.\n\nBest regards,\nThe {(website.name).capitalize()} Team"

                    email_thread3 = threading.Thread(target=send_email, args=(subject1, body1, transfer_user.email))
                    email_thread3.start()

                    email_thread3.start()
                except Exception as e:
                    print(e)
                messages.success(request, 'You have made a transfer')
                return redirect('/transfer')
        except Exception as e:
            print(e)
            messages.error(request, 'There was an error with your transaction')
            return redirect('/transfer')
    
    # Move these lines outside of the POST request handling for efficiency
    user = request.user
    transfers = Transfer.objects.filter(user=user).order_by('-created')[:5]
    
    context = {
        'user': user,
        'transfers': transfers,
    }
    
    return render(request, 'user/transfer.html', context)


