# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = DJENV['DJ_ALLOWED_HOSTS']

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': DJENV['DB_NAME'],
		'USER': DJENV['DB_USER'],
		'PASSWORD': DJENV['DB_PASS'],
		'HOST': 'localhost',
		'PORT': '5432'
	}
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = [
	BASE_DIR / 'static',
	'/www/ditra.com/static/',
]

# # STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
STATIC_ROOT = DIR_PROD / 'static'


# Media files (Images, xls, word, pdf, etc...)

MEDIA_URL = '/media/'

MEDIA_ROOT = DIR_PROD / 'media'