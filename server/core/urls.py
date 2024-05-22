from . import views
from django.urls import path

# URL pattern for about
urlpatterns = [

path('dashboard/', views.about, name='about'),
]