from .models import Website
from django.conf import settings

def website (request):
    try:
        site, created  = Website.objects.get_or_create(id=1)
    except Exception as e:
        site = Website.objects.create(id=1)
        site.save()
    return { 'website': site}

def configs(request):
    
    if settings.GOOGLE_TRANSLATE_LINK and settings.CHAT_BOT:
        return {
            'google_translate_link' : settings.GOOGLE_TRANSLATE_LINK,
            'chat_bot' : settings.CHAT_BOT,
        }
    else:
        return {
            'google_translate_link' : None,
            'chat_bot' : None,
        }
