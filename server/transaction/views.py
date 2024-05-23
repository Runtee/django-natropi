from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from userprofile.decorators import check_profile_exists
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction

# Create your views here.
@login_required(login_url='/accounts/login')
@check_profile_exists
def user_transaction(request):    
    profile = Profile.objects.get(user=request.user)
    
    category = request.GET.get('category')
    if category:
        transactions = Transaction.objects.filter(profile=profile,transaction_type=category).order_by('-created')
    else:
        transactions = Transaction.objects.filter(profile=profile).order_by('-created')
    
    context = {
        'transactions':transactions,
        
    }
    return render(request,'user/transaction.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_transaction(request):
    transactions = Transaction.objects.all()

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_transaction_completed(request):
    transactions = Transaction.objects.filter(verified=True)

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction2.html',context)

@login_required(login_url='/accounts/login')
@can_access_dashboard
def dashboard_transaction_pending(request):
    transactions = Transaction.objects.filter(verified=False)

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction2.html',context)