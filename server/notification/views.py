from django.shortcuts import render,redirect
from utils import  can_access_dashboard
from django.contrib.auth import get_user_model
User = get_user_model()
from userprofile.models import Profile
from .models import Notification
from userprofile.decorators import check_profile_exists
from walletaddress.models import WalletAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from transaction.models import Transaction
from django.conf import settings

# Create your views here.


def user_notification(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    
    # Get all unread notifications
    notifications_unreads = Notification.objects.filter(profile=profile, read=False).order_by('-created')
    
    # Get all notifications (including both read and unread)
    notifications = Notification.objects.filter(profile=profile).exclude(id__in=notifications_unreads.values_list('id', flat=True)).order_by('-created')
    
    # Mark unread notifications as read
    for notification in notifications_unreads:
        notification.read = True
        notification.save()
    
    # Get the latest 3 unread notifications
    notifications_unread = notifications_unreads[:3]
    
    
    context = {
        'notifications': notifications,
        'profile': profile,
        'notifications_unreads': notifications_unreads,
        'notifications_unread_count': len(notifications_unreads),
        'notifications_unread': notifications_unread,
    }
    return render(request, 'user/notification.html', context)