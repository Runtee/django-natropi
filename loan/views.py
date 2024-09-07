from django.shortcuts import render, get_object_or_404
from .models import LoanTerm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from kyc.models import KYC
from deposit.models import Deposit

def loan_term_list(request):
    loan_terms = LoanTerm.objects.all() 
    context = {'loan_terms': loan_terms}
    return render(request, 'user/loan.html', context)


def loan_term_detail(request, pk):
    """
    View to display the details of a specific loan term.
    """
    loan_term = get_object_or_404(LoanTerm, pk=pk)
    return render(request, 'user/loan.html', {'loan_term': loan_term})


def filter_by_amount(request):
    """
    Function-based view to filter loan terms by loan amount.
    Example usage: /filter-by-amount/?min_amount=50000&max_amount=100000
    """
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')

    if min_amount and max_amount:
        loan_terms = LoanTerm.objects.filter(min_amount__gte=min_amount, max_amount__lte=max_amount)
    else:
        loan_terms = LoanTerm.objects.all()

    return render(request, 'user/loan.html', {'loan_terms': loan_terms})


def filter_by_credit_score(request):
    """
    Function-based view to filter loan terms by credit score requirement.
    Example usage: /filter-by-credit-score/?credit_score=650
    """
    credit_score = request.GET.get('credit_score')

    if credit_score:
        loan_terms = LoanTerm.objects.filter(credit_score_min__lte=credit_score)
    else:
        loan_terms = LoanTerm.objects.all()

    return render(request, 'user/loan.html', {'loan_terms': loan_terms})



@login_required
def apply_term1(request, pk):
    loan_term = get_object_or_404(LoanTerm, pk=pk)
    
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None

    has_deposit = Deposit.objects.filter(user=request.user).exists()
    
    if kyc and kyc.status != 'verified':
        messages.error(request, 'Your KYC has not been verified. Please complete the KYC process before applying for a loan.')
        return redirect('submit_kyc')

    if not has_deposit:
        messages.error(request, 'You need to make a deposit to apply for a loan.')
        return render(request, 'user/deposit.html')  # Redirect to a page where users can make a deposit

    # If both conditions are met, proceed to the loan application page with loan term details
    return render(request, 'user/loan_apply1.html', {'loan_term': loan_term})

@login_required
def apply_term2(request, pk):
    loan_term = get_object_or_404(LoanTerm, pk=pk)
    
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None

    has_deposit = Deposit.objects.filter(user=request.user).exists()
    
    if kyc and kyc.status != 'verified':
        messages.error(request, 'Your KYC has not been verified. Please complete the KYC process before applying for a loan.')
        return redirect('submit_kyc')

    if not has_deposit:
        messages.error(request, 'You need to make a deposit to apply for a loan.')
        return render(request, 'user/deposit.html')  # Redirect to a page where users can make a deposit

    # If both conditions are met, proceed to the loan application page with loan term details
    return render(request, 'user/loan_apply2.html', {'loan_term': loan_term})