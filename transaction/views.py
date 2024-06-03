from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction

# Create your views here.
@login_required(login_url='/login')
def user_transaction(request):    
    user=request.user
    
    category = request.GET.get('category')
    if category:
        transactions = Transaction.objects.filter(user=user,transaction_type=category).order_by('-created')
    else:
        transactions = Transaction.objects.filter(user=user).order_by('-created')
    
    context = {
        'transactions':transactions,
        
    }
    return render(request,'user/transactions.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_transaction(request):
    transactions = Transaction.objects.all()

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_transaction_completed(request):
    transactions = Transaction.objects.filter(verified=True)

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction2.html',context)

@login_required(login_url='/login')
@can_access_dashboard
def dashboard_transaction_pending(request):
    transactions = Transaction.objects.filter(verified=False)

    context = {
        'transactions':transactions,
        
    }
    return render(request,'dashboard/transaction2.html',context)