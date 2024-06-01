from django.urls import path
from . import views

urlpatterns = [
    path('withdraw-form/', views.withdraw_view, name='withdraw_view'),
]
