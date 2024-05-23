from django.db import models
from django.contrib.auth.models import User

class Fund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    trans_hash = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(default=1)

class NumAcc(models.Model):
    status = models.CharField(max_length=1)
    # other fields as per your requirements
