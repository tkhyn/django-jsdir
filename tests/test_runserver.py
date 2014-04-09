"""
Tests the app in expanded mode
"""

import os

from base import JSDirTestCase

from django.template.loader import render_to_string
from django.conf import settings


class JSDirRunserverTests(JSDirTestCase):
    # run tests in runserver mode (i.e. using staticfile finders)
    # the JS directories should be expanded

    use_finders = True

    def test_expanded_runserver(self):

        self.set_use_finders(True)
        generated = render_to_string('jsdir.%shtml' % \
            ('dj' if settings.SET == 'django' else 'jj'), {})

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        # running with debug = False, so libs are minified
        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.min.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.min.js"></script>']
        )

    def test_expanded_runserver_debug(self):

        self.set_debug(True)

        self.set_use_finders(True)
        generated = render_to_string('jsdir.%shtml' % \
            ('dj' if settings.SET == 'django' else 'jj'), {})

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        # running with debug = True, so libs are not minified
        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.js"></script>']
        )
