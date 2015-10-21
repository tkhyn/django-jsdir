import os
import shutil

from django.conf import settings

from ._base import JSDirTestCase, with_template_engines


@with_template_engines('Django', 'Jinja2')
class JSDirProdTests(JSDirTestCase):

    use_finders = False

    def setUp(self):
        super(JSDirProdTests, self).setUp()
        app_static = os.path.join(os.path.dirname(__file__), 'app', 'static')
        shutil.copytree(os.path.join(app_static, 'js'),
                        os.path.join(settings.STATIC_ROOT, 'js'))

    def tearDown(self):
        super(JSDirProdTests, self).tearDown()
        shutil.rmtree(os.path.join(settings.STATIC_ROOT, 'js'))

    def test_concat(self):
        generated = self.render_to_string('jsdir')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertTrue(os.path.isfile(os.path.join(js_dir,
                                                    'big_script.dir.js')))
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        bs = open(os.path.join(js_dir, 'big_script.dir.js'), 'r')
        bs_ctnt = bs.read().splitlines()
        bs.close()
        self.assertListEqual(bs_ctnt,
            ["var x1 = 'file1';",
             "var x2 = 'file2';",
             "var x3 = 'file3';"])

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script.dir.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.min.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.min.js"></script>']
        )

    def test_expanded(self):
        # in debug mode, the JS Dir is expected to be expanded
        self.set_debug(True)
        generated = self.render_to_string('jsdir')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/big_script/01-file1.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/02-file2.js"></script>',
             '<script type="text/javascript" src="/static/js/big_script/03-file3.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib2.js"></script>',
             '<script type="text/javascript" src="/static/js/libs/lib1.js"></script>']
        )

    def test_exclude_concat(self):
        # setting debug mode to False so that the directory is concatenated
        self.set_debug(False)
        generated = self.render_to_string('exclude')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        libs_dir_js = os.path.join(js_dir, 'libs.dir.js')
        self.assertTrue(os.path.exists(libs_dir_js))

        lib_dir = open(libs_dir_js, 'r')
        lib_dir_ctnt = lib_dir.read().splitlines()
        lib_dir.close()
        self.assertListEqual(lib_dir_ctnt,
            ["var lib2 = 'lib2';"])

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/libs.dir.js"></script>']
        )

    def test_exclude_debug(self):
        # setting debug mode to True so that the directory is expanded
        self.set_debug(True)
        generated = self.render_to_string('exclude')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/libs/lib2.js"></script>']
        )

    def test_include_concat(self):
        # setting debug mode to False so that the directory is concatenated
        self.set_debug(False)
        generated = self.render_to_string('include')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        libs_dir_js = os.path.join(js_dir, 'libs.dir.js')
        self.assertTrue(os.path.exists(libs_dir_js))

        lib_dir = open(libs_dir_js, 'r')
        lib_dir_ctnt = lib_dir.read().splitlines()
        lib_dir.close()
        self.assertListEqual(lib_dir_ctnt,
            ["var lib1 = 'lib1';"])

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/libs.dir.js"></script>']
        )

    def test_include_debug(self):
        # setting debug mode to True so that the directory is expanded
        self.set_debug(True)
        generated = self.render_to_string('include')

        js_dir = os.path.join(settings.STATIC_ROOT, 'js')
        self.assertFalse(os.path.exists(os.path.join(js_dir, 'libs.js')))

        self.assertListEqual(generated.strip().splitlines(),
            ['<script type="text/javascript" src="/static/js/libs/lib1.js"></script>']
        )
