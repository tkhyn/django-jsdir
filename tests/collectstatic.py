import os
import shutil

from ._base import JSDirTestCase

from django.core.management import call_command
from django.conf import settings


class CollectStaticTests(JSDirTestCase):

    def tearDown(self):
        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        if os.path.exists(js_dir):
            shutil.rmtree(js_dir)

    def test_first_call(self):
        call_command('collectstatic', interactive=False, verbosity=0)

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')

        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))

        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        self.assertListEqual(os.listdir(os.path.join(js_dir, 'big_script')),
                             os.listdir(os.path.join(os.path.dirname(__file__),
                                                     'app', 'static', 'js',
                                                     'big_script')))

    def test_generate(self):

        call_command('collectstatic', interactive=False, verbosity=0)

        # DEBUG and JSDir.use_finder[this thread] are False by default

        # this should generate the big_script.dir.js file
        self.render_to_string('jsdir')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')

        self.assertTrue(os.path.exists(os.path.join(js_dir,
                                                    'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

    def test_regenerate(self):

        self.test_generate()

        path = os.path.join(settings.STATIC_ROOT, 'js', 'big_script.dir.js')
        mtime = os.stat(path).st_mtime

        # this should regenerate big_script.dir.js
        call_command('collectstatic', interactive=False, verbosity=0)

        # test that the modification time for big_script.dir.js has changed
        self.assertNotEqual(mtime, os.stat(path).st_mtime)
