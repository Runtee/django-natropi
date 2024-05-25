from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_referral, name="user_referral")
]