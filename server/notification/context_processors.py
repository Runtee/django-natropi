from .models import Notification
from userprofile.models import Profile

def notification(request):
    try:
        profile = Profile.objects.get(user=request.user)
        notifications_unreads = Notification.objects.filter(profile=profile, read=False).order_by('-created')
        # Get the latest 3 unread notifications
        notifications_unread = notifications_unreads[:3]
        notifications_unread_count = len(notifications_unreads)
        
    except Exception as e:
        notifications_unread_count = {},
        notifications_unread = {}
        print(e)
    return {  
        'notifications_unread_count': notifications_unread_count,
        'notifications_unread': notifications_unread
        }