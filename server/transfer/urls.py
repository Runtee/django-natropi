from django.urls import path
from .views import *

urlpatterns = [
    path('transfer-form/', transfer_view, name='transfers'),
    path('p2p-transfer/', p2p_transfer_view, name='transfer_success'),
    path('p2p/', p2p, name='p2p'),
    path('p2p_form/', p2p_form, name='p2p_form'),

]
