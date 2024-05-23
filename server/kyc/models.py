from django.db import models
from userprofile.models import Profile
# Create your models here.

    
class Kyc(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    country = models.CharField(max_length=100,null=True,blank=True)
    ids_type = models.FileField(upload_to='kyc_ids', default='kyc.pdf',null=True,blank=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)    
    address = models.CharField(max_length=300,null=True,blank=True)
    proof_of_address = models.FileField(upload_to='kyc_documents',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    class Meta:
        verbose_name = "Kyc"
        verbose_name_plural = "Kyc"
        ordering = ['-created']
    def __str__(self):
        return f'{self.first_name} has submitted documents for kyc' 