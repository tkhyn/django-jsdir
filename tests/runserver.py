"""
Tests the app in expanded mode
"""

import os

from django.conf import settings

from ._base import JSDirTestCase, with_template_engines


@with_template_engines('Django', 'Jinja2')
class JSDirRunserverTests(JSDirTestCase):
    # run tests in runserver mode (i.e. using staticfile finders)
    # the JS directories should be expanded

    use_finders = True

    def test_expanded_runserver(self):

        generated = self.render_to_string()

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        # running with debug = False, so libs are minified
        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" '
                'src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/libs/lib2.min.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/libs/lib1.min.js"></script>']
        )

    def test_expanded_runserver_debug(self):

        self.set_debug(True)

        generated = self.render_to_string()

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir,
                                                     'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        # running with debug = True, so libs are not minified
        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" '
                'src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/libs/lib2.js"></script>',
             '<script type="text/javascript" '
                'src="/static/js/libs/lib1.js"></script>']
        )
