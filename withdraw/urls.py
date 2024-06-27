from django.urls import path
from . import views

urlpatterns = [
    path('', views.withdrawal, name='withdraw'),
    path('withdrawal_form/', views.withdraw_view, name='withdrawal_form'),
    path('verify/<int:id>', views.verify, name="verify_withdrawal"),

]
