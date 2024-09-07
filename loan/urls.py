from django.urls import path
from . import views

urlpatterns = [
    path('loan-terms/', views.loan_term_list, name='loan_term_list'),
    path('loan-terms/<int:pk>/', views.loan_term_detail, name='loan_term_detail'),
    path('filter-by-amount/', views.filter_by_amount, name='filter_by_amount'),
    path('filter-by-credit-score/', views.filter_by_credit_score, name='filter_by_credit_score'),
    path('loan/apply-term1/<int:pk>/', views.apply_term1, name='apply_term'),
    path('loan/apply-term2/<int:pk>/', views.apply_term2, name='apply_term2'),
]
