# from utils.util import send_email
from utils import send_email
from celery import shared_task

@shared_task
def send_email_task(subject,body,recipient):
    return send_email(subject,body,recipient)