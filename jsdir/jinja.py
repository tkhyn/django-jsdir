"""
Jinja2 extension to provide a {% jsdir %} tag
"""

from jinja2 import nodes
from jinja2.ext import Extension

from core import JSDir


class JinjaTag(Extension):
    """
    Base class for a simple tag returning a constant string
    """

    tags = set(['jsdir'])

    def parse(self, parser):
        parser.stream.next()
        args = []
        while parser.stream.current.type != 'block_end':
            args.append(parser.parse_expression())
        return nodes.Output([self.call_method('get_tags', args)])

    def get_tags(self, path):
        return JSDir(path).get_tags()


ext = JinjaTag
