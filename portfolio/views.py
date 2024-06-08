# portfolio/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Portfolio, PortfolioAdd
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation

User = get_user_model()

@login_required(login_url='/login')
def portfolioAddListView(request):
    portfolioTypes = PortfolioAdd.objects.values_list('type', flat=True).distinct()

    typeitem = {}
    for type in portfolioTypes:
        typeitem[type] = list(PortfolioAdd.objects.filter(type=type))

    context = {
        'types': list(portfolioTypes),
        'typeitem': typeitem
    }

    return render(request, 'user/portfolio.html', context)

@login_required(login_url='/login')
def portfolioAddGetView(request, id):
    portfolioAdd = get_object_or_404(PortfolioAdd, id=id)
    context = {"portfolio": portfolioAdd}
    return render(request, 'user/portfolio_view.html', context)

@login_required(login_url='/login')
def port_invest(request, id):
    portfolioAdd = get_object_or_404(PortfolioAdd, id=id)
    context = {"portfolio": portfolioAdd}

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
        except InvalidOperation:
            message = "Invalid amount entered"
            return render(request, 'user/port_invest.html', {"portfolio": portfolioAdd, 'message': message})

        user = request.user
        if user.portfolio >= amount:
            user.portfolio -= amount
            user.save()

            portfolio = Portfolio.objects.create(
                user=user,
                date=timezone.now().strftime('%Y-%m-%d'),
                amount=amount,
                portfolioadd=portfolioAdd
            )

            # Schedule the investment
            from .scheduler import schedule_weekly_profit, schedule_investment_completion
            schedule_weekly_profit(portfolio)
            schedule_investment_completion(portfolio)

            return redirect('/portfolio/port_invest_table')
        else:
            message = "Insufficient Portfolio Amount"
            return render(request, 'user/port_invest.html', {"portfolio": portfolioAdd, 'message': message})

    return render(request, 'user/port_invest.html', context)

@login_required(login_url='/login')
def port_invest_table(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {"portfolio": portfolio}
    return render(request, 'user/port_invest_table.html', context)
