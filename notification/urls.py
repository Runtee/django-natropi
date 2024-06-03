from django.urls import path
from . import views

urlpatterns = [
   path('',views.user_notification, name='user_notification'),
]
