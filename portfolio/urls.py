from django.urls import path
from .views import *

urlpatterns = [
    path('', portfolioAddListView, name='portfolio'),
    path('<int:id>', portfolioAddGetView, name='portfolio_view'),
    path('port_invest/<int:id>', port_invest, name='port_invest'),
    path('port_invest_table', port_invest_table, name='port_invest_table'),
]
