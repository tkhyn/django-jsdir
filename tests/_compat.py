import django


if django.VERSION >= (1, 8):
    JINJA_TEMPLATE_SETTINGS = dict(
        TEMPLATES=dict(
            BACKEND='djinga.backends.djinga.DjingaTemplates',
            OPTIONS=dict(
                extensions='jsdir.jinja2.ext',
            )
        )
    )
else:
    # old-style template settings
    JINJA_TEMPLATE_SETTINGS = dict(
        TEMPLATE_LOADERS=(
            'djinga.loaders.FileSystemLoader',
            'djinga.loaders.AppLoader',
        ),
        JINJA2_EXTENSIONS=(
            'jsdir.jinja2.ext',
        )
    )
