from website.models import Website
from django.shortcuts import render


def about(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': "site",
    }
    return render(request, 'user/profile.html', context)


def get_started(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'get-started.html', context)


def index(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'index.html', context)


def about_3(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'about-3.html', context)


def faq(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'faq.html', context)


def login(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'login.html', context)


def register(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'register.html', context)


def forgot_password(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'forgot-password.html', context)


def contact(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'contact.html', context)


def api(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'api.html', context)


def change_password(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'user/new-password.html', context)

def withdrawal(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'user/withdraw.html', context)


def withdrawal_form(request):
    try:
        site = Website.objects.get(pk=1)
    except Website.DoesNotExist:
        site = Website.objects.create(pk=1)
        site.save()
    context = {
        'site': site,
    }
    return render(request, 'user/withdraw_form.html', context)