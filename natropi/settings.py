"""
Django settings for natropi project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^&d+h5b@u&yfp&*2^^ph%xmsimjiy4!4b4d8$+h67dfqqi*r%l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #    'django.contrib.sites',
    'django.contrib.humanize',
    'mathfilters',
    'core.apps.CoreConfig',
    'accounts',
    'website',
    'deposit',
    'walletaddress',
    'transaction',
    'notification',
    'transfer',
    'referral',
    'user',
    'portfolio',
    'loan',
    'withdraw',
    'crispy_bootstrap4', 
    'kyc',
    'crispy_forms',
    'django_recaptcha'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'natropi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.website',
                'website.context_processors.configs',
                'notification.context_processors.notification',
            ],
        },
    },
]

WSGI_APPLICATION = 'natropi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    "default": dj_database_url.config(default='postgresql://postgres:xstrUmYfgwJAcnFDKALJoevrbYzrpOGn@postgres.railway.internal:5432/railway', conn_max_age=1800),
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('DBNAME_DEV'),
#         'USER': env('DATABASE_USER'),
#         'HOST': env('DATABASE_HOST'),
#         'PORT': env('DATABASE_PORT'),
#         'PASSWORD' : env('DATABASE_PASSWORD')
#     }
# }


CSRF_TRUSTED_ORIGINS = ['https://natropi.up.railway.app/', 'https://natropi.up.railway.app', 'https://natropi.com', 'https://natropi.com/', 'https://www.natropi.com/','https://www.natropi.com']


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = 'optional'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_URL = '/login'

LOGIN_REDIRECT_URL = '/user/'

#ACCOUNT_SIGNUP_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')


#i installed django_smtp_ssl to use 'django_smtp_ssl.SSLEmailBackend'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'support@natropi.com'
EMAIL_HOST_PASSWORD = 'Clara1995unn_cheap_support'
DEFAULT_FROM_EMAIL = 'support@natropi.com'

# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# # Custom setting. To email
RECIPIENT_ADDRESS = 'Tajadaryan@gmail.com'



GOOGLE_TRANSLATE_LINK="https://translate.google.com/intl/en/about/website/"
CHAT_BOT="https://translate.google.com/intl/en/about/website/"

# Message tags for Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
# DISABLE_COLLECTSTATIC= 0

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Recaptcha Settings
RECAPTCHA_PUBLIC_KEY = '6Ld0WZoqAAAAAIFVbhR1oKNWvf88GhkPEGpl-iMk'
RECAPTCHA_PRIVATE_KEY = '6Ld0WZoqAAAAAPlBWjfJnpXAnkXXXytlPjiIW_OP'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
