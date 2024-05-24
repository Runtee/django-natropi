from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from website.models import Website
from django.contrib.auth.models import User

# def check_type(request,value,value_type):
#     print('using a function')
#     print(type(value))
#     print(value)
#     if isinstance(value,value_type):
#         return value
#     else:
#         print('function dtxg')
#         return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
def send_email(subject,body,recipient):
    site, created = Website.objects.get_or_create(pk=1)
    name = site.name
    address = site.address
    phone_number = site.phone_number
    email = site.email
    logo = site.logo.url
    context ={
        "title": subject,
        "content":body,
        "name": name,
        "address": address,
        "phone_number":phone_number,
        "email": email,
        "logo":logo
        }   
    html_content = render_to_string("other/temp.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER ,
        [recipient]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=False)
    

def can_access_dashboard(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            user = request.user
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/user/')
        except Exception as e:
            print('dashboard error')
            print(e)
            return redirect('/user/')
    return wrapped_view
