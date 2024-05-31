from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_dashboard, name='user_dashboard'),
        path('update-profile/', views.update_profile, name='update_profile'),
        path('change-password/', views.change_password, name='change_password'),

]