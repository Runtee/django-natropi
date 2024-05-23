from django.urls import path
from .views import DepositIndexView, DepositCreateView, DepositStoreView, WithdrawIndexView, WithdrawCreateView, WithdrawStoreView, TransferIndexView, TransferCreateView, TransferStoreView

urlpatterns = [
    path('deposit/', DepositIndexView.as_view(), name='deposit'),
    path('deposit/create/', DepositCreateView.as_view(), name='deposit_create'),
    path('deposit/store/', DepositStoreView.as_view(), name='deposit_store'),
    path('withdraw/', WithdrawIndexView.as_view(), name='withdraw'),
    path('withdraw/create/', WithdrawCreateView.as_view(), name='withdraw_create'),
    path('withdraw/store/', WithdrawStoreView.as_view(), name='withdraw_store'),
    path('transfer/', TransferIndexView.as_view(), name='transfer'),
    path('transfer/create/', TransferCreateView.as_view(), name='transfer_create'),
    path('transfer/store/', TransferStoreView.as_view(), name='transfer_store'),
]
