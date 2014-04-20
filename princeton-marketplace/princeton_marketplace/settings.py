"""
Django settings for demosite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h_haz1=^4rm+q**nbrz+$px*vf5jsun9u*#@g@40cel(_4(z4j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["www.princeton-marketplace.appspot.com"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'market',
    'south',
    'parsley',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

ROOT_URLCONF = 'princeton_marketplace.urls'

WSGI_APPLICATION = 'princeton_marketplace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/princeton-marketplace:market',
            'NAME': 'market',
            'USER': 'root',
        }
    }

else:
    # Running in development, but want to access the Google Cloud SQL instance
    # in production.
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'google.appengine.ext.django.backends.rdbms',
    #         'INSTANCE': 'princeton-marketplace:market',
    #         'NAME': 'market',
    #         'USER': 'root',
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'market',
            'USER': 'root',
            'PASSWORD': 'root'
        }
    }

    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.mysql'}

# Upload Handler for Files to Blobstore
FILE_UPLOAD_HANDLERS = ('market.storagewrapper.BlobstoreFileUploadHandler',)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, "market/static"),
    )
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# CAS login information
CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_VERSION = '1'
