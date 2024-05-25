from allauth.account.signals import user_logged_in,user_signed_up
from django.dispatch.dispatcher import receiver
from django.conf import settings
from accounts.models import CustomUser
import threading
from utils import send_email
#smail



@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    subject = 'Login Sucessful,Welcome back to our site'
    body = f"Dear {request.user.username}, We're glad to see you back on our website! We hope you had a great time since your last visit.Don't hesitate to reach out to us if you have any questions or need help with anything. Our customer support team is always here to assist you.Enjoy your time on our site!Best regards,{request.user.username}"
    userprofile = CustomUser.objects.filter(user = request.user)
    
    try:
        userprofile = CustomUser.objects.get(user = request.user)
       
        if userprofile.loginemailblocked:
            pass
        else:
            try:
                try:
                    email_thread = threading.Thread(target=send_email,args=(subject,body,request.user.email))
                    email_thread.start()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
    
    except CustomUser.DoesNotExist:
        pass
        
    
    
      
     
        
@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    subject = 'Signup Sucessful,Welcome to our site'
    body_two = f"Dear {user.username},Thank you for signing up for our website! We're excited to have you as a member and look forward to providing you with a great experience.If you have any questions or need help navigating our site, please don't hesitate to reach out to us. Our customer support team is here to assist you.In the meantime, take a look around and see all of the great features and benefits that we have to offer. We're sure you'll find something you love.Best regards,{user.username}"
    body = f"Dear Admin, The new user {user.username} has signed up"
    try:
        if user.email:
            try:
                email_thread = threading.Thread(target=send_email,args=(subject,body_two,user.email))
                email_thread.start()
            except Exception as e:
                print(e)
        try:
            email_thread = threading.Thread(target=send_email,args=(subject,body,settings.RECIPIENT_ADDRESS))
            email_thread.start()
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)