# -*- coding: utf-8 -*-

"""
Django settings for the edem project.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7u&!5zoikcssm7a2a2xifvwxjg&7akumk0op3*i37u6%)n97n+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'django_admin_bootstrapped', # bootstrap that admin !
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_gravatar', # django-gravatar2
	'auth_with_one_time_code',
	'accueil',
	'membres',
	'fichiers_adherents',
	'tableau_de_bord',
	'aggregateur',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'edem.urls'

WSGI_APPLICATION = 'edem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Template location

TEMPLATE_DIRS = (
	os.path.join((BASE_DIR), "static", "templates"),
)

if DEBUG:
	
	STATIC_ROOT = os.path.join((BASE_DIR), "static", "static-only")
	MEDIA_ROOT = os.path.join((BASE_DIR), "static", "media")
	STATICFILES_DIRS = (
		os.path.join((BASE_DIR), "static", "static"),
	)

from django.contrib import messages
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = messages.DEBUG

MESSAGE_TAGS = { messages.ERROR: 'danger' }

LOGIN_URL = 'connexion'
LOGOUT_URL = 'deconnexion'
LOGIN_REDIRECT_URL = 'accueil'

AUTHENTICATION_BACKENDS = ('auth_with_one_time_code.backend.OneTimeCodeBackend',)

EMAIL_SUBJECT_PREFIX = "[Élan Démocrate] "
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "antonin.grele@gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = '5Bluepotatoes'
