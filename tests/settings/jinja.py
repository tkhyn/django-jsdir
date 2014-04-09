from common import *

SET = 'jinja'

INSTALLED_APPS += (
    'djinga',
)

TEMPLATE_LOADERS = (
    'djinga.loaders.FileSystemLoader',
    'djinga.loaders.AppLoader',
)
