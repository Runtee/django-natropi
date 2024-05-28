from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
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
    bank_address = models.CharField(max_length=255, blank=True, null=True)
    sort_code = models.CharField(max_length=255, blank=True, null=True)
    main = models.BigIntegerField(default=0)
    portfolio = models.BigIntegerField(default=0)
    strategy = models.BigIntegerField(default=0)
    trade = models.BigIntegerField(default=0)
    image = models.ImageField(blank=True, null=True)
    status = models.CharField(max_length=255, default='1')
    remember_token = models.CharField(max_length=100, blank=True)
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


# class PasswordReset(models.Model):
#     email = models.EmailField(db_index=True)
#     token = models.CharField(max_length=255)
#     created_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return self.email


# class FailedJob(models.Model):
#     uuid = models.CharField(max_length=255, unique=True)
#     connection = models.TextField()
#     queue = models.TextField()
#     payload = models.TextField()
#     exception = models.TextField()
#     failed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.uuid


# class PersonalAccessToken(models.Model):
#     tokenable_type = models.CharField(max_length=255)
#     tokenable_id = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     token = models.CharField(max_length=64, unique=True)
#     abilities = models.TextField(blank=True, null=True)
#     last_used_at = models.DateTimeField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Fund(models.Model):
#     user_id = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     method = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     trans_hash = models.CharField(max_length=255)
#     date = models.CharField(max_length=255)
#     amount = models.CharField(max_length=255)
#     status = models.CharField(max_length=255, default='0')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class FundAdd(models.Model):
#     name = models.CharField(max_length=255)
#     amount = models.CharField(max_length=255)
#     status = models.CharField(max_length=255, default='1')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Transaction(models.Model):
#     user_id = models.CharField(max_length=255)
#     date = models.CharField(max_length=255)
#     type = models.CharField(max_length=255)
#     from_field = models.CharField(max_length=255, db_column='from')
#     to = models.CharField(max_length=255)
#     message = models.CharField(max_length=255)
#     amount = models.CharField(max_length=255)
#     status = models.CharField(max_length=255, default='0')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user_id


# class Portfolio(models.Model):
#     user_id = models.CharField(max_length=255)
#     date = models.CharField(max_length=255)
#     amount = models.BigIntegerField()
#     portfolioadd_id = models.CharField(max_length=255)
#     staamounttus = models.CharField(max_length=255, default='1')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user_id


# class PortfolioAdd(models.Model):
#     name = models.CharField(max_length=255)
#     type = models.CharField(max_length=255, blank=True, null=True)
#     header = models.CharField(max_length=255, blank=True, null=True)
#     min_invest = models.CharField(max_length=255, blank=True, null=True)
#     invest_time = models.CharField(max_length=255, blank=True, null=True)
#     horizon = models.CharField(max_length=255, blank=True, null=True)
#     term = models.CharField(max_length=255, blank=True, null=True)
#     level_of_risk = models.CharField(max_length=255, blank=True, null=True)
#     conservation = models.CharField(max_length=255, blank=True, null=True)
#     short_term = models.CharField(max_length=255, blank=True, null=True)
#     image = models.CharField(max_length=255, blank=True, null=True)
#     port_stock1 = models.CharField(max_length=255, blank=True, null=True)
#     port_stock2 = models.CharField(max_length=255, blank=True, null=True)
#     port_stock3 = models.CharField(max_length=255, blank=True, null=True)
#     port_stock4 = models.CharField(max_length=255, blank=True, null=True)
#     port_weight1 = models.CharField(max_length=255, blank=True, null=True)
#     port_weight2 = models.CharField(max_length=255, blank=True, null=True)
#     port_weight3 = models.CharField(max_length=255, blank=True, null=True)
#     port_weight4 = models.CharField(max_length=255, blank=True, null=True)
#     port_returns1 = models.CharField(max_length=255, blank=True, null=True)
#     port_returns2 = models.CharField(max_length=255, blank=True, null=True)
#     port_returns3 = models.CharField(max_length=255, blank=True, null=True)
#     port_returns4 = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=255, default='1')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Trade(models.Model):
#     date = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     user_id = models.CharField(max_length=255)
#     amount = models.BigIntegerField()
#     close_date = models.CharField(max_length=255)
#     protection_level = models.CharField(max_length=255)
#     safty_mode = models.CharField(max_length=255)
#     trade_type = models.CharField(max_length=255)
#     status = models.CharField(max_length=255, default='0')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class StrategyAdd(models.Model):
#     name = models.CharField(max_length=255)
#     numbers = models.CharField(max_length=255)
#     amount = models.BigIntegerField()
#     percentage = models.CharField(max_length=255)
#     image = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=255, default='1')
#     close_date = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name


# class Strategy(models.Model):
#     user_id = models.CharField(max_length=255)
#     stra_id = models.CharField(max_length=255)
#     date = models.CharField(max_length=255)
#     amount = models.CharField(max_length=255)
#     profit = models.CharField(max_length=255, default='0')
#     roi = models.BigIntegerField()
#     outcome = models.CharField(max_length=255, default='')
#     paid = models.CharField(max_length=255, default='0')
#     status = models.CharField(max_length=255, default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user_id


# class Acct(models.Model):
#     method = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     name = models.CharField(max_length=255, blank=True, null=True)
#     acct_name = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=255, default='1')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.method
