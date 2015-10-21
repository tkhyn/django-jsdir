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
    'jsdir',
    'django.contrib.staticfiles',
    'djinga',
    'django_nose',
    'tests.app',
)

MIDDLEWARE_CLASSES = ()

STATIC_URL = '/static/'
STATIC_ROOT = tempfile.mkdtemp('_jsdir')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
