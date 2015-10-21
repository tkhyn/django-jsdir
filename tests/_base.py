"""
Base test class
"""

import sys
import os
import shutil

from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from django.template.loader import get_template

from djinga.engines import engines

from jsdir.core import JSDir

from ._compat import JINJA_TEMPLATE_SETTINGS

__test__ = False


TEMPLATE_ENGINE_SETTINGS = {
    'Django': ('djhtml', None),
    'Jinja2': ('jjhtml', JINJA_TEMPLATE_SETTINGS)
}


def with_template_engines(*args):
    """
    Decorator that creates copies of the created class so that tests are
    run against other template engines
    """

    def mk_classes(cls):
        module = sys.modules[cls.__module__]
        name = cls.__name__
        for te in args:
            try:
                te_settings = TEMPLATE_ENGINE_SETTINGS[te][1]
            except (KeyError, TypeError):
                continue

            new_name = '%s_%s' % (name, te)
            if te_settings is None:
                cls.__name__ = new_name
            else:
                te_class = override_settings(**te_settings)(type(new_name,
                                                                 (cls,), {}))
                setattr(module, new_name, te_class)
                te_class.engine = TEMPLATE_ENGINE_SETTINGS[te][0]

        return cls

    return mk_classes


class JSDirTestCase(TestCase):

    use_finders = False
    debug = False

    # default template file extension for django templates
    ext = 'djhtml'

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(settings.STATIC_ROOT):
            os.mkdir(settings.STATIC_ROOT)
        try:
            engines._engines = {}
        except AttributeError:
            # django <= 1.7
            pass

    @classmethod
    def tearDownClass(cls):
        # cleanup
        shutil.rmtree(settings.STATIC_ROOT)

    def setUp(self):
        self.set_debug(self.debug)
        self.set_use_finders(self.use_finders)

    def tearDown(self):
        self.set_debug(False)
        self.set_use_finders(False)

    def set_debug(self, value):
        settings.DEBUG = value

    def set_use_finders(self, value):
        JSDir.set_use_finders(value)

    def render_to_string(self, template_name, context=None):
        if context is None:
            context = {}
        tmpl = get_template('%s.%s' % (template_name, self.ext))
        try:
            return tmpl.render(context)
        except AttributeError:
            # django <= 1.7
            from django.template import Context
            return tmpl.render(Context(context))
