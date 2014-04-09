import os
import shutil

from django.conf import settings
from django.template.loader import render_to_string

from base import JSDirTestCase


class JSDirProdTests(JSDirTestCase):

    use_finders = False

    def setUp(self):
        super(JSDirProdTests, self).setUp()
        app_static = os.path.join(os.path.dirname(__file__), 'static')
        shutil.copytree(os.path.join(app_static, 'js'),
                        os.path.join(settings.STATIC_ROOT, 'js'))

    def tearDown(self):
        super(JSDirProdTests, self).tearDown()
        shutil.rmtree(os.path.join(settings.STATIC_ROOT, 'js'))

    def test_concat(self):
        generated = render_to_string('jsdir.%shtml' % \
            ('dj' if settings.SET == 'django' else 'jj'), {})

        big_script = \
            os.path.join(settings.STATIC_ROOT, 'js', 'big_script.dir.js')
        self.assertTrue(os.path.isfile(big_script))

        bs = open(big_script, 'r')
        self.assertListEqual(bs.read().splitlines(),
            ["var x1 = 'file1';",
             "var x2 = 'file2';",
             "var x3 = 'file3';"])
        bs.close()

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script.dir.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.min.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.min.js"></script>']
        )

    def test_expanded(self):
        # in debug mode, the JS Dir is expected to be expanded
        self.set_debug(True)
        generated = render_to_string('jsdir.%shtml' % \
            ('dj' if settings.SET == 'django' else 'jj'), {})

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.js"></script>']
        )
