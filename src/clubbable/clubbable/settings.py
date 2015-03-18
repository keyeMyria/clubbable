"""
Django settings for clubbable project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+o6khsst!&j2pp3!d#&=2s7!$ra4g$xjipwfw%vpqc_eqt2jwo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'club',
    'notices',
    'website',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'clubbable.urls'

WSGI_APPLICATION = 'clubbable.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# clubbable-specific settings
# Title by which to refer to members, e.g. "Rotarian". None if not applicable
MEMBER_TITLE = 'Owl'

# Mail settings for outgoing mail
SMTP_SERVER = 'localhost'
SMTP_PORT = 0  # 0 = Default
FROM_ADDRESS = 'The Club Webmaster <webmaster@example.com>'
REPLY_TO_ADDRESS = 'The Club Secretary <secretary@example.com>'  # Optional
BOUNCE_ADDRESS = '<bounce@example.com>'  # Optional

# Import settings for local deployment, if applicable
try:
    from settings_local import *
except ImportError:
    pass
