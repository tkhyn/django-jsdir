from django import template

from ..core import JSDir

register = template.Library()


@register.simple_tag
def jsdir(path):
    return JSDir(path).get_tags()
