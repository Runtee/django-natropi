from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Portfolio, PortfolioAdd
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def portfolioAddListView(request):
    portfolioTypes = PortfolioAdd.objects.values_list(
        'type', flat=True).distinct()

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

    context = {"portfolio": portfolioAdd
               }

    return render(request, 'user/portfolio_view.html', context)



@login_required(login_url='/login')
def port_invest(request, id):
    portfolioAdd = get_object_or_404(PortfolioAdd, id=id)

    context = {"portfolio": portfolioAdd
               }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        port_amount = request.user.portfolio
        if port_amount > int(amount):
            message = "Successfully Added"
            user = User.objects.get(pk=request.user.id)
            user.portfolio -= int(amount)
            user.save()
            mydate = timezone.now()
            portfolio = Portfolio()
            portfolio.user = request.user
            portfolio.date = mydate
            portfolio.amount = int(amount)
            portfolio.portfolioadd_id = request.POST.get('port_id')
            portfolio.save()
            portfolio_list = Portfolio.objects.filter(user=request.user)
            return redirect('/portfolio/port_invest_table')
        else:
            message = "Insufficient Portfolio Amount"
            portfolio_list = Portfolio.objects.filter(user=request.user)
            return render(request, 'user/port_invest.html', {"portfolio": portfolioAdd, 'message': message})

    return render(request, 'user/port_invest.html',context)

@login_required(login_url='/login')
def port_invest_table(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {"portfolio": portfolio}

    return render(request, 'user/port_invest_table.html',context)
