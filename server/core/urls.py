from . import views
from django.urls import path

# URL pattern for about
urlpatterns = [

    path('dashboard/', views.about, name='about'),

    # URL pattern for get_started
    path('get_started/', views.get_started, name='get_started'),

    # URL pattern for index
    path('index/', views.index, name='index'),

    # URL pattern for about_3
    path('about/', views.about_3, name='about_3'),

    # URL pattern for faq
    path('faq/', views.faq, name='faq'),

    # URL pattern for login
    path('login/', views.login, name='login'),

    # URL pattern for register
    path('register/', views.register, name='register'),

    # URL pattern for forgot_password
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    # URL pattern for contact
    path('contact/', views.contact, name='contact'),

    # URL pattern for api
    path('api/', views.api, name='api'),
]
