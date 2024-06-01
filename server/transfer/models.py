from django.db import models
from accounts.models import CustomUser

class Transfer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    from_wallet = models.CharField(max_length=50)
    to_wallet = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of ${self.amount} from {self.from_wallet} to {self.to_wallet} by {self.user.username} on {self.date}"
