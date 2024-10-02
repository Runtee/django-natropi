from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    CustomPasswordResetDoneView,
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),

    path('logout/', views.Logout.as_view(), name='logout')

]
    
