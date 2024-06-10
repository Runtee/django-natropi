# portfolio/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Portfolio, PortfolioAdd
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from notification.models import Notification
from utils.util import send_email
from website.models import Website
import threading

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
    website,_ = Website.objects.get_or_create(id=1)
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
            notification = Notification.objects.create(user=user, action=f'{portfolioAdd.header.capitalize()}', description=f'You have successfully applied for the {portfolioAdd.header} plan')
            notification.save()
            try:
                email_subject = portfolioAdd.header
                email_body = f"Dear {user.username},\n\nThank you for applying for the {portfolioAdd.header} plan. Your request has been received, and our team will review it promptly. We appreciate your interest in our services and look forward to serving you with the selected plan.\n\nBest regards,\nThe {(website.name).capitalize()} Team"
                email_thread = threading.Thread(target=send_email, args=(email_subject, email_body, request.user.email))
                email_thread.start()
            except Exception as e:
                print(e)
            

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
