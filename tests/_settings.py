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
    'jsdir',
    'django_nose',
    'tests.app',
)

STATIC_URL = '/static/'
STATIC_ROOT = tempfile.mkdtemp('_jsdir')

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# only used for jinja tests
JINJA2_EXTENSIONS = (
    'jsdir.jinja.ext',
)
