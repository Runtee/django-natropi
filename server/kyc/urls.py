from django.urls import path
from . import views
urlpatterns = [
        path('',views.user_kyc, name='user_kyc'),
                path('verify/<int:id>', views.verify, name="verify_transaction")

]