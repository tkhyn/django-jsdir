django-jsdir - changes
======================


v0.2 (07-01-2015)
-----------------

- `first` and `last` keywords now use Unix-like patterns instead of plain names
- `jsdir.jinja.ext` is now available under `jsdir.jinja2.ext`
- adds `exclude` keyword support

v0.2.1 (16-04-2015)
...................
- Django 1.8 support


0.1 (09-04-2014) - beta
-----------------------

- Birth!
- collectstatic and runserver management commands overrides
- django and jinja2 tags

0.1.1 (10-04-2014) - beta
.........................

- 'expand' keyword for always expanded directories
- 'minify' keyword to prevent automatic minification


0.1.2 (10-04-2014) - beta
.........................

- adds 'first' and 'last' keywords to amend order of files in expanded dirs
- using process id rather than thread id
- performance improvements

0.1.3 (19-11-2014)
..................

- test management command override
- Django 1.7 compatibility
- Python 3 compatibility
