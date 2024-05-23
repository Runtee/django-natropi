from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_deposit, name='user_deposit'),
        path('user/deposit/completed',views.user_deposit_completed, name='user_deposit_completed'),
        path('user/deposit/pending',views.user_deposit_pending, name='user_deposit_pending'),
        path('verify/<int:id>', views.verify, name="verify_transaction"),
        path('dashboard/deposit',views.dashboard_deposit, name='dashboard_deposit'),
        path('dashboard/deposit/completed',views.dashboard_deposit_completed, name='dashboard_deposit_completed'),
        path('dashboard/deposit/pending',views.dashboard_deposit_pending, name='dashboard_deposit_pending'),
        path('delete/deposit/<int:id>',views.delete_deposit, name='delete_deposit'),
]