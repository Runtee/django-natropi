from django.db import models

# Create your models here.

class Website(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True,default='Blank Name')
    email = models.EmailField(null=True,blank=True,default='Blank Email')
    address = models.CharField(max_length=300,null=True,blank=True,default='Blank Address')
    second_address = models.CharField(max_length=300,null=True,blank=True,default='Blank Address')
    logo = models.ImageField(upload_to='site_images', default='logo.png')
    phone_number = models.CharField(max_length=25,null=True,blank=True)
    minimum_withdrawal = models.FloatField(default=0,null=True,blank=True)
    maximum_withdrawal = models.FloatField(default=0,null=True,blank=True)
    owned_by = models.CharField(max_length=50,null=True,blank=True,default='Admin')
    
    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Website'
        
    
    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f'{self.name}'

class Statistics(models.Model):
    runingdays = models.IntegerField(null=True,blank=True, )
    extradeposit = models.IntegerField(null=True,blank=True,)
    extrawithdrawal = models.IntegerField(null=True,blank=True,)
    extrausers = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return "extra stats"
    
 