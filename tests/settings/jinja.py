DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'jsdir',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'jsdir',
    'djinga',
    'tests',
)
