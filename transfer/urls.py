from django.urls import path
from .views import *

urlpatterns = [
    path('', transfer, name='transfers'),
    path('transfer-form/', transfer_view, name='transfer_form'),
    path('p2p/', p2p, name='p2p'),
    path('p2p-form/', p2p_transfer_view, name='p2p_form'),
]
