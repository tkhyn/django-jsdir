"""
Runs the tests with the matching settings set
"""

import shutil
from importlib import import_module


def run(settings_set):

    print('\n\nRunning tests with %s settings\n' % settings_set)

    SETTINGS = import_module('tests.settings.' + settings_set)
    from django.conf import settings, empty

    settings._wrapped = empty
    settings.configure(**{k: getattr(SETTINGS, k) for k in dir(SETTINGS) \
                              if k[0].isupper()})

    from django.test.simple import DjangoTestSuiteRunner

    test_runner = DjangoTestSuiteRunner(verbosity=1)
    test_runner.run_tests(['tests', ])

    shutil.rmtree(settings.STATIC_ROOT)
