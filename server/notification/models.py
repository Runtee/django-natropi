from django.db import models
from userprofile.models import Profile
# Create your models here.

class Notification(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    action = models.TextField(blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return f'{self.profile.user.username} - {self.action}'  