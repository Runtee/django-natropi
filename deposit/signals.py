from django.dispatch import Signal, async_dispatcher
from transaction.models import Transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Deposit

my_async_signal = Signal(async_dispatcher=True)

@receiver(my_async_signal, sender=Deposit)
async def my_async_signal_handler(sender, instance,**kwargs):
    # Your asynchronous handling logic here
    # For example, you can use async IO operations or other asynchronous tasks
    print('ready')
    # if instance.verified:
    #     transaction = Transaction.objects.get(id=transcation_id)
    #     transaction.verified
    #     transaction.save()
        
#celery for post save and async signals for views

