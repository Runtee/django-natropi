from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Fund, NumAcc
from .forms import FundForm, WithdrawForm, TransferForm

@method_decorator(login_required, name='dispatch')
class DepositIndexView(View):
    def get(self, request):
        deposits = Fund.objects.filter(name="Deposit", user_id=request.user.id)
        return render(request, 'dash/deposit_table.html', {'deposits': deposits})

@method_decorator(login_required, name='dispatch')
class DepositCreateView(View):
    def get(self, request):
        numacc = NumAcc.objects.filter(status="1")
        return render(request, 'dash/deposit_form.html', {'numacc': numacc, 'numacc1': numacc})

@method_decorator(login_required, name='dispatch')
class DepositStoreView(View):
    def post(self, request):
        form = FundForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            fund.user = request.user
            fund.name = "Deposit"
            fund.date = timezone.now()
            fund.save()
            return redirect('deposit')
        return render(request, 'dash/deposit_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class WithdrawIndexView(View):
    def get(self, request):
        withdrawals = Fund.objects.filter(name="Withdraw", user_id=request.user.id)
        return render(request, 'dash/withdraw_table.html', {'withdrawals': withdrawals})

@method_decorator(login_required, name='dispatch')
class WithdrawCreateView(View):
    def get(self, request):
        return render(request, 'dash/withdraw_form.html')

@method_decorator(login_required, name='dispatch')
class WithdrawStoreView(View):
    def post(self, request):
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet_type = form.cleaned_data['wallet']
            user = request.user
            if wallet_type == "main" and user.main < amount:
                message = "Insufficient wallet funds Main"
            elif wallet_type == "portfolio" and user.portfolio < amount:
                message = "Insufficient wallet funds Portfolio"
            elif wallet_type == "strategy" and user.strategy < amount:
                message = "Insufficient wallet funds Strategy"
            elif wallet_type == "trade" and user.trade < amount:
                message = "Insufficient wallet funds Trade"
            else:
                if wallet_type == "main":
                    user.main -= amount
                elif wallet_type == "portfolio":
                    user.portfolio -= amount
                elif wallet_type == "strategy":
                    user.strategy -= amount
                elif wallet_type == "trade":
                    user.trade -= amount
                
                user.save()
                fund = Fund(
                    user=user,
                    name="Withdraw",
                    method=wallet_type,
                    address=form.cleaned_data['method'],
                    trans_hash="Withdrawal hash",
                    date=timezone.now(),
                    amount=amount,
                    status=0
                )
                fund.save()
                message = "Successful"
            return render(request, 'dash/withdraw_form.html', {'message': message})
        return render(request, 'dash/withdraw_form.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class TransferIndexView(View):
    def get(self, request):
        transfers = Fund.objects.filter(name="Transfer", user_id=request.user.id)
        return render(request, 'dash/transfer_table.html', {'transfers': transfers})

@method_decorator(login_required, name='dispatch')
class TransferCreateView(View):
    def get(self, request):
        return render(request, 'dash/transfer_form.html')

@method_decorator(login_required, name='dispatch')
class TransferStoreView(View):
    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_wallet = form.cleaned_data['from']
            to_wallet = form.cleaned_data['to']
            user = request.user
            if from_wallet == to_wallet:
                message = "You can't transfer to the same account"
            elif from_wallet == "main" and user.main < amount:
                message = "Insufficient wallet funds Main"
            elif from_wallet == "portfolio" and user.portfolio < amount:
                message = "Insufficient wallet funds Portfolio"
            elif from_wallet == "strategy" and user.strategy < amount:
                message = "Insufficient wallet funds Strategy"
            elif from_wallet == "trade" and user.trade < amount:
                message = "Insufficient wallet funds Trade"
            else:
                if from_wallet == "main":
                    user.main -= amount
                elif from_wallet == "portfolio":
                    user.portfolio -= amount
                elif from_wallet == "strategy":
                    user.strategy -= amount
                elif from_wallet == "trade":
                    user.trade -= amount
                
                if to_wallet == "main":
                    user.main += amount
                elif to_wallet == "portfolio":
                    user.portfolio += amount
                elif to_wallet == "strategy":
                    user.strategy += amount
                elif to_wallet == "trade":
                    user.trade += amount
                
                user.save()
                fund = Fund(
                    user=user,
                    name="Transfer",
                    method=from_wallet,
                    address=to_wallet,
                    trans_hash="Within",
                    date=timezone.now(),
                    amount=amount,
                    status=1
                )
                fund.save()
                message = "Successful"
            return render(request, 'dash/transfer_form.html', {'message': message})
        return render(request, 'dash/transfer_form.html', {'form': form})

