"""
Base test class
"""

from unittest import TestCase

from django.conf import settings

from jsdir.core import JSDir


class JSDirTestCase(TestCase):

    use_finders = False
    debug = False

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
