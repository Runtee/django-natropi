from django.urls import path
from .views import transfer_view

urlpatterns = [
    path('transfer-form/', transfer_view, name='transfers'),
]
