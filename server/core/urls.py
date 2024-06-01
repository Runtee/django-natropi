from . import views
from django.urls import path

# URL pattern for about
urlpatterns = [
    path('p2p/', views.p2p, name='p2p'),
    path('p2p_form/', views.p2p_form, name='p2p_form'),

    # URL pattern for get_started
    path('get_started/', views.get_started, name='get_started'),

    # URL pattern for index
    path('', views.index, name='index'),

    # URL pattern for about_3
    path('about/', views.about_3, name='about_3'),

    # URL pattern for faq
    path('faq/', views.faq, name='faq'),


    # URL pattern for forgot_password
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    # URL pattern for contact
    path('contact/', views.contact, name='contact'),

    # URL pattern for api
    path('api/', views.api, name='api'),

    # URL pattern for change_password
    path('change_password/', views.change_password, name='change_password'),
]
