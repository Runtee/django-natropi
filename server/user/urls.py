from django.urls import path
from . import views

urlpatterns = [
        path('update-profile/', views.update_profile, name='update_profile'),
        path('change-password/', views.change_password, name='change_password'),

]