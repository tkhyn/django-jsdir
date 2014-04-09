import os
import shutil
from unittest import TestCase

from django.core.management import call_command
from django.conf import settings
from django.template.loader import render_to_string


class CollectStaticTests(TestCase):

    def tearDown(self):
        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        if os.path.exists(js_dir):
            shutil.rmtree(js_dir)

    def test_first_call(self):
        call_command('collectstatic', interactive=False, verbosity=0)

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')

        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))
        self.assertListEqual(os.listdir(os.path.join(js_dir, 'big_script')),
                             os.listdir(os.path.join(os.path.dirname(__file__),
                                                     'static', 'js',
                                                     'big_script')))

    def test_generate(self):

        call_command('collectstatic', interactive=False, verbosity=0)

        # DEBUG and JSDir.use_finder[this thread] are False by default

        # this should generate the big_script.dir.js file
        render_to_string('jsdir.%shtml' % \
            ('dj' if settings.SET == 'django' else 'jj'), {})

        self.assertTrue(os.path.exists(os.path.join(settings.STATIC_ROOT, 'js',
                                                    'big_script.dir.js')))

    def test_regenerate(self):

        self.test_generate()

        path = os.path.join(settings.STATIC_ROOT, 'js', 'big_script.dir.js')
        mtime = os.stat(path).st_mtime

        # this should regenerate big_script.dir.js
        call_command('collectstatic', interactive=False, verbosity=0)

        # test that the modification time for big_script.dir.js has changed
        self.assertNotEqual(mtime, os.stat(path).st_mtime)
