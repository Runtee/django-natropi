from django.shortcuts import render, get_object_or_404
from walletaddress.models import Acct
from .models import LoanApplication, LoanTerm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from kyc.models import KYC
from deposit.models import Deposit
from django.urls import reverse
from decimal import Decimal
from .models import LoanTerm, Upfront, Loan 
from django.utils import timezone
from datetime import timedelta, datetime


def loan_term_list(request):
    # Check if the user has any loan applications
    pending_loan = LoanApplication.objects.filter(user=request.user).first()

    if pending_loan:
        if pending_loan.status == 'pending':
            # Add a message to inform the user
            messages.warning(request, "You have a pending loan application that has not been approved yet.")
            # Redirect to the loan status page for the pending loan
            return redirect('loan_status', pk=pending_loan.pk)  # Pass the pk of the pending loan

        elif pending_loan.status == 'approved':
            # Check if the user has made an upfront payment
            upfront_payment = Upfront.objects.filter(user=request.user, loan_amount_requested=pending_loan.loan_amount).exists()

            if not upfront_payment:
                # Redirect to the upfront payment page
                messages.info(request, "Your loan has been approved. Please complete the upfront payment.")
                return redirect('user_upfront_form', pk=pending_loan.pk)

    # Continue to loan terms if no pending or approved loans
    loan_terms = LoanTerm.objects.all()  # Assuming you have a LoanTerm model for listing loan terms
    return render(request, 'user/loan.html', {'loan_terms': loan_terms})



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

    # Check if the user already has an active or pending loan application
    existing_loan = LoanApplication.objects.filter(user=request.user, status__in=['approved', 'pending']).exists()
    
    if existing_loan:
        messages.error(request, 'You already have an active or pending loan application and cannot apply for another one.')
        return redirect('loan_dashboard')
    
    if kyc and kyc.status != 'verified':
        messages.error(request, 'Your KYC has not been verified. Please complete the KYC process before applying for a loan.')
        return redirect('submit_kyc')

    if not has_deposit:
        messages.error(request, 'You need to make a deposit to apply for a loan.')
        return redirect('deposit_form')  # Redirect to a page where users can make a deposit

    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount'))
        deposit_amount = loan_amount * 0.03  # 3% deposit

        # Create and save the loan application
        loan_application = LoanApplication.objects.create(
            user=request.user,
            loan_term=loan_term,
            loan_amount=loan_amount,
            
        )

        
        # Pass the deposit amount and loan amount to the template
        context = {
            'loan_term': loan_term,
            'loan_amount': loan_amount,
            'deposit_amount': deposit_amount
        }
        messages.success(request, 'Your loan application has been submitted successfully and is pending approval.')
        return redirect('loan_status', pk=loan_application.pk)
    return render(request, 'user/loan_apply1.html', {'loan_term': loan_term})



@login_required
def loan_status(request, pk):
    loan_application = get_object_or_404(LoanApplication, user=request.user, pk=pk)
    
    if loan_application.status == 'approved':
        # Redirect to the next page, i.e., upfront payment form page
        return redirect('user_upfront_form', pk=loan_application.pk)
    
    return render(request, 'user/loan_status.html', {'loan_application': loan_application})



@login_required
def apply_term2(request, pk):
    loan_term = get_object_or_404(LoanTerm, pk=pk)
    
    try:
        kyc = KYC.objects.get(user=request.user)
    except KYC.DoesNotExist:
        kyc = None

    has_deposit = Deposit.objects.filter(user=request.user).exists()

    # Check if the user already has an active or pending loan application
    existing_loan = LoanApplication.objects.filter(user=request.user, status__in=['approved', 'pending']).exists()
    
    if existing_loan:
        messages.error(request, 'You already have an active or pending loan application and cannot apply for another one.')
        return redirect('loan_dashboard')

    
    if kyc and kyc.status != 'verified':
        messages.error(request, 'Your KYC has not been verified. Please complete the KYC process before applying for a loan.')
        return redirect('submit_kyc')

    if not has_deposit:
        messages.error(request, 'You need to make a deposit to apply for a loan.')
        return redirect('deposit_form')

    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount'))
        deposit_amount = loan_amount * 0.03  # 3% deposit

        # Create and save the loan application
        loan_application = LoanApplication.objects.create(
            user=request.user,
            loan_term=loan_term,
            loan_amount=loan_amount,
           
        )

        messages.success(request, 'Your loan application has been submitted successfully and is pending approval.')
        return redirect('loan_status', pk=loan_application.pk)

    return render(request, 'user/loan_apply2.html', {'loan_term': loan_term})


@login_required
def user_upfront_form(request, pk):
    """
    View for handling the upfront payment form and loan creation.
    """
    # Fetch the loan application using the primary key (pk)
    loan_application = get_object_or_404(LoanApplication, pk=pk, user=request.user)
    loan_amount_requested = loan_application.loan_amount  # Retrieve the loan amount from LoanApplication

    if request.method == 'POST':
        try:
            method = request.POST.get('method')
            trans_hash = request.POST.get('trans_hash')
        except (TypeError, ValueError):
            messages.error(request, 'Invalid input.')
            return redirect('loan_dashboard')

        # Validate KYC
        try:
            kyc = KYC.objects.get(user=request.user)
            if kyc.status != 'verified':
                messages.error(request, 'Your KYC is not verified. Please complete it before proceeding.')
                return redirect('submit_kyc')
        except KYC.DoesNotExist:
            messages.error(request, 'Please complete the KYC process before applying.')
            return redirect('submit_kyc')

        # Calculate upfront payment (3% of the loan amount from LoanApplication)
        upfront_amount = loan_amount_requested * Decimal('0.03')

        # Save the upfront payment in the database
        upfront = Upfront.objects.create(
            user=request.user,
            amount=upfront_amount,
            method=method,
            transaction_hash=trans_hash,
            loan_amount_requested=loan_amount_requested  # Save the loan amount
        )

        # Check if a loan already exists for this user
        try:
            loan = Loan.objects.get(user=request.user)
        except Loan.DoesNotExist:
            # If no loan exists, create a new one for the user
            loan_term = loan_application.loan_term.repayment_term_min  # Use loan term from loan application

            loan = Loan.objects.create(
                user=request.user,
                amount_requested=loan_amount_requested,
                amount_paid=upfront_amount,  # Set initial payment
                repayment_term_months=loan_term,
                applied_date=datetime.now().date()
            )

        # Associate the upfront payment with the loan
        loan.upfronts.add(upfront)
        loan.amount_paid += upfront_amount  # Update the loan's paid amount
        loan.save()

        messages.success(request, 'Upfront payment submitted and loan created/updated successfully!')
        return redirect('loan_dashboard')

    else:
        # Fetch the loan term information for display if needed
        upfront_amount = loan_amount_requested * Decimal('0.03')  # Calculate upfront amount (3% of loan)

        numacc = Acct.objects.filter(status="1")  # Fetch account status or other needed data

        context = {
            'upfront_amount': upfront_amount,
            'numacc': numacc,
            'loan_application': loan_application,  # Pass loan application to the template if needed
        }
        return render(request, 'user/upfront.html', context)







@login_required
def loan_dashboard(request):
    try:
        # Fetch the latest loan application for the logged-in user
        loan_application = LoanApplication.objects.filter(user=request.user).latest('created_at')
        
        # Get the loan amount from the LoanApplication model
        loan_amount = loan_application.loan_amount

        # Calculate the upfront payment (3% of the loan amount)
        upfront_payment = loan_amount * Decimal('0.03')

        # Calculate the remaining balance (loan amount minus upfront payment)
        loan_balance = loan_amount

        # Assuming the repayment term is in months, fetch it from the loan application or loan model
        remaining_months = loan_application.loan_term.repayment_term_min  # Adjust based on your logic
        
        total_paid = upfront_payment  # Total paid so far (just the upfront amount for now)

    except LoanApplication.DoesNotExist:
        loan_application = None
        loan_amount = 0
        loan_balance = 0
        remaining_months = 0
        total_paid = 0

    context = {
        'loan_application': loan_application,
        'loan_amount': loan_amount,
        'loan_balance': loan_balance,
        'remaining_months': remaining_months,
        'total_paid': total_paid,
    }

    return render(request, 'user/loan_dashboard.html', context)

