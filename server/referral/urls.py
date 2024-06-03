from django.urls import path
from . import views

urlpatterns = [
    path('referrals/', views.user_referrals, name='user_referrals'),
]
