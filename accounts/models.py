import uuid
from django.db import models
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

def profile_image_path(instance, filename):
    return os.path.join('img', filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Set is_active to True for superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    dob = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    bit_wallet = models.CharField(max_length=255, blank=True, null=True)
    ussdc_wallet = models.CharField(max_length=255, blank=True, null=True)
    paypal_address = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    bank_address = models.CharField(max_length=255, blank=True, null=True)
    sort_code = models.CharField(max_length=255, blank=True, null=True)
    main = models.BigIntegerField(default=0)
    portfolio = models.BigIntegerField(default=0)
    strategy = models.BigIntegerField(default=0)
    trade = models.BigIntegerField(default=0)
    image = models.ImageField(upload_to=profile_image_path, null=True, default='assets/img/logo/logo.jpg')
    status = models.CharField(max_length=255, default='1')
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

