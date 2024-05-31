from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Portfolio, PortfolioAdd
from django.utils import timezone


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


def portfolioAddGetView(request, id):

    portfolioAdd = get_object_or_404(PortfolioAdd, id=id)

    context = {"portfolio": portfolioAdd
               }

    return render(request, 'user/portfolio_view.html', context)



def port_invest(request, id):
    portfolioAdd = get_object_or_404(PortfolioAdd, id=id)

    context = {"portfolio": portfolioAdd
               }
    if request.method == 'POST':
        amount = request.POST.get('amount')
        port_amount = request.user.portfolio
        if port_amount > amount:
            message = "Successfully Added"
            user = User.objects.get(pk=request.user.id)
            user.portfolio -= amount
            user.save()
            mydate = timezone.now()
            portfolio = Portfolio()
            portfolio.user = request.user
            portfolio.date = mydate
            portfolio.amount = amount
            portfolio.portfolioadd_id = request.POST.get('port_id')
            portfolio.save()
            portfolio_list = Portfolio.objects.filter(user=request.user)
            return redirect('portfolio/port_invest_table')
        else:
            message = "Insufficient Portfolio Amount"
            portfolio_list = Portfolio.objects.filter(user=request.user)
            return render(request, 'dash/port_invest.html', {'portfolio': portfolio_list, 'message': message})

    return render(request, 'user/port_invest.html',context)

def port_invest_table(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {"portfolio": portfolio}

    return render(request, 'user/port_invest_table.html',context)
