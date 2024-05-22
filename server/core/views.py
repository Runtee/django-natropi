from django.shortcuts import render
import threading
from django.contrib import messages
from django.conf import settings

def about(request):
    # try:
    #     site = Website.objects.get(pk=1)
    # except Website.DoesNotExist:
    #     site = Website.objects.create(pk=1)
    #     site.save()
    context = {
        'site': "site",
    }
    return render(request, 'user/profile.html', context)
