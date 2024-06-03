from django.shortcuts import render
from .models import Notification

# Create your views here.


def user_notification(request):
    user = request.user
    
    # Get all unread notifications
    notifications_unreads = Notification.objects.filter(user=user, read=False).order_by('-created')
    
    # Get all notifications (including both read and unread)
    notifications = Notification.objects.filter(user=user).exclude(id__in=notifications_unreads.values_list('id', flat=True)).order_by('-created')
    
    # Mark unread notifications as read
    for notification in notifications_unreads:
        notification.read = True
        notification.save()
    
    # Get the latest 3 unread notifications
    notifications_unread = notifications_unreads[:3]
    
    
    context = {
        'notifications': notifications,
        'user': user,
        'notifications_unreads': notifications_unreads,
        'notifications_unread_count': len(notifications_unreads),
        'notifications_unread': notifications_unread,
    }
    return render(request, 'user/notification.html', context)