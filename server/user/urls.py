from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_dashboard, name='dashboard'),
        path('profile',views.user_dashboard, name='profile'),
        path('update-profile/', views.update_profile, name='update_profile'),
        path('change-password/', views.change_password, name='change_password'),

]