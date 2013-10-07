import os
from datetime import timedelta

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_TZ = True
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'static'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'thecleanest.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'south',
    'postmark',
    'tastypie',
    'mathfilters',
    'thecleanest.schedule',
    'thecleanest.notifications',
    'gunicorn',
)

EMAIL_BACKEND = "postmark.backends.PostmarkBackend"
EMAIL_SENDER = "Cleanosaurus Rex <cleanosaurusrex@sunlightfoundation.com>"
EMAIL_RECIPIENT = None

API_LIMIT_PER_PAGE = 100

NUDGE_GRACE_PERIOD = timedelta(minutes=30)
SCHED_HORIZON = 31
EXCUSED = [
    'jturk@sunlightfoundation.com',
    'paultag@sunlightfoundation.com',
    'tneale@sunlightfoundation.com',
    'ethan@sunlightfoundation.com',
    'bpease@sunlightfoundation.com',
    'tknuutila@sunlightfoundation.com',
    'showell@sunlightfoundation.com',
]
