from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_transaction, name='user_transaction'),
    path('dashboard', views.dashboard_transaction, name='dashboard_transaction'),
    path('dashboard/completed', views.dashboard_transaction_completed, name='dashboard_transaction_completed'),
    path('dashboard/pending', views.dashboard_transaction_pending, name='dashboard_transaction_pending'),
]