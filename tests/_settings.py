import tempfile

DEBUG = True
SECRET_KEY = 'secret'

DATABASES = {
    'default': {
        'NAME': 'jsdir',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'djinga',
    'django_nose',
    'tests.app',
)

import django
if django.VERSION < (1, 7):
    INSTALLED_APPS += ('jsdir',)
else:
    # django 1.7 reversed the management commands override priority order
    INSTALLED_APPS = ('jsdir',) + INSTALLED_APPS

MIDDLEWARE_CLASSES = ()

STATIC_URL = '/static/'
STATIC_ROOT = tempfile.mkdtemp('_jsdir')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
