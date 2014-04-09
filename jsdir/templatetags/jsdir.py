from django import template

from ..core import JSDir

register = template.Library()


@register.simple_tag
def jsdir(path):

    # expand directory
    is_absolute = path.startswith('/') or ':' in path.split('/')[0]
    if is_absolute:
        raise NotImplementedError('jsdir: absolute urls like %s are not '
                                  'supported' % path)

    return JSDir(path).get_tags()
