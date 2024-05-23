from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_withdrawal, name='withdrawal'),
    path('user/withdraw/completed',views.user_withdraw_completed, name='user_withdraw_completed'),
        path('user/withdraw/pending',views.user_withdraw_pending, name='user_withdraw_pending'),
    path('verify/<int:id>', views.verify, name="verify_transaction"),
    path('dashboard/withdraw',views.dashboard_withdraw, name='dashboard_withdraw'),
        path('dashboard/withdraw/completed',views.dashboard_withdraw_completed, name='dashboard_withdraw_completed'),
        path('dashboard/withdraw/pending',views.dashboard_withdraw_pending, name='dashboard_withdraw_pending'),
        path('delete/withdraw/<int:id>',views.delete_withdraw, name='delete_withdraw'),
]
