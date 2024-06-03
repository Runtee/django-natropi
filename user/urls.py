from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_dashboard, name='dashboard'),
        path('profile/', views.update_profile, name='profile'),
        path('change-password/', views.change_password, name='change_password'),

]