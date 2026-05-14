from django.shortcuts import redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from website.models import Website
from django.contrib.auth import get_user_model
import resend

# def check_type(request,value,value_type):
#     print('using a function')
#     print(type(value))
#     print(value)
#     if isinstance(value,value_type):
#         return value
#     else:
#         print('function dtxg')
#         return redirect(request.META.get('HTTP_REFERER', '/'))
    
    
resend.api_key = settings.RESEND_API_KEY


def send_email(subject: str, body: str, recipient: str):
    site, created = Website.objects.get_or_create(pk=1)
    name = site.name
    address = site.address
    phone_number = site.phone_number
    email = site.email
    logo = site.logo.url
    context = {
        "title": subject,
        "content": body,
        "name": name,
        "address": address,
        "phone_number": phone_number,
        "email": email,
        "logo": logo,
    }
    html_content = render_to_string("other/temp.html", context)
    text_content = strip_tags(html_content)
    params: resend.Emails.SendParams = {
        "from": "Natropi <support@natropi.com>",
        "to": [recipient],
        "subject": subject,
        "html": html_content,
    }

    try:
        email = resend.Emails.send(params)
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")


def resend_email_api(subject: str, html_content: str, recipient: str):
    params: resend.Emails.SendParams = {
        "from": "Natropi <support@natropi.com>",
        "to": [recipient],
        "subject": subject,
        "html": html_content,
    }

    try:
        email = resend.Emails.send(params)
        return email
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")
        return None

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
