django-jsdir
============

|copyright| 2014-2015 Thomas Khyn, MIT License


About
-----

When your project tightly depends on a relatively large amount of JavaScript
code, the natural way of dealing with it is to break the JavaScript code down
into several sub-scripts. This both improves readability and ease of debugging.

However, there are times when you would be happy to only have one - possibly
compressed - file (in production for example) or to not have to link every
single standalone js file in your template in development.

django-jsdir aims at solving this issue by providing a way to automatically
link the js files in a directory tree with a single template tag.

django-jsdir works with django 1.6 to 1.8, from python 2.6 to 3.4.


Setup
-----

1. Install using your prefered method, e.g ``pip install django-jsdir``
2. You will need both ``'jsdir'`` and ``'django.contrib.staticfiles'`` in your
   ``INSTALLED_APPS``. If you are using Django 1.6, make sure that ``'jsdir'``
   is placed `after` ``'django.contrib.staticfiles'``. If you are using Django
   1.7, ``'jsdir'`` must be placed `before` ``'django.contrib.staticfiles'``.
3. If you are using Jinja2, add ``'jsdir.jinja2.ext'`` to your Jinja2
   extensions list


How it works
------------

Directory concatenation
.......................

A short real-life example is better than long boring explanations. Suppose you
have the following JS files layout::

    static/js/
        big_script/
            00_init.js
            10_helpers.js
            50_core.js
            99_onload.js

All the files in big_script are nicely formatted and commented javascript
files, perfect for debugging. But you have to include each js file from
big_script in your template. And even worse, when deploying your application,
you need to concatenate/compress the big_script directory and update your
template accordingly. All that entirely manually.

Until now.

With django-jsdir and a few minimal changes, you will not have to worry about
that anymore. The only thing to do is to get rid of all the ``<script>`` tags
refering to big_script/\*.js files in your template, and replace them by::

    {% jsdir 'big_script' %}

django-jsdir will then take care of:

1. linking all the scripts nested under big_script directory tree when in
   development mode with files served from the application's static directory.
   This will change nothing from the developer's point of view, except he won't
   need to update the script list anymore
2. concatenating (and possibly compressing, with the help of
   django-compressor_) all the nested subscripts in one file named
   `big_script.dir.js` either on the first request or when you'll run
   ``manage.py collectstatic``, depending if the file already exists or not
3. linking the generated `big_script.dir.js` when in production mode

In other words, you do not have to change your production template (or scratch
your head to find a way to do it programmatically with conditional extends or
includes) AND you do not have to manually concatenate and/or compress your JS
files anymore.


.. warning:: As in JS, the order in which the files are loaded matters, it is
   worth noting that the concatenation order will be alphabetic. Use numbers
   with a fixed number of digits to name your JS files, for example.

.. note:: If a directory bar.js is nested into a foo.js directory, no bar.js
   file will be generated. All the files in the bar.js directory will be
   concatenated in the foo.js file.


Inclusion of all files in a directory
.....................................

Sometimes, you will prefer to import the javascript files from a directory
without seeing them concatenated at all. It is the case if you have a 'lib'
folder containing javascript librairies. In that situation, you may use the
tag argument ``expand``::

   {% jsdir 'lib/' expand=True %}

In production (i.e. with ``DEBUG = False``), jsdir will look for minified
versions of the scripts (files named \*.min.js) and return corresponding HTML
tags. If you don't want this behavior, you can use the tag argument
``minified`` and set it to ``False``::

   {% jsdir 'lib' expand=True minified=False %}

Remember that the order in which the HTML tags will appear in the document,
and therefore the order in which the JS files will be loaded is still
alphabetic. You can however ask django-jsdir to load certain files first or
last.

If subdirectories or files in subdirectories must be excluded from the lookup,
you may use the ``exclude`` keyword, which uses Unix-like patterns (see
fnmatch_). The following line will exclude all the files in lib and its
subdirectories that ends with ``'-to_exclude.js'``::

   {% jsdir 'lib' exclude='*-to_exclude.js' %}


``first`` and ``last`` keywords
+++++++++++++++++++++++++++++++

In case you want to load some files first in the included expanded directory,
django-jsdir provides the ``first`` and ``last`` keywords.

Use them like that::

   {% jsdir 'lib' expand=True first='1st_pattern; 2nd_pattern' last='verylast_parttern; 2ndtolast_pattern' %}

Any file which name matches the glob pattern '1st_pattern' will be loaded
before any file which name matches '2nd_pattern', which will be loaded before
any other file, which will be loaded before any file which name matches
'2ndtolast_pattern', which will be loaded before any file which name matches
'verylast_pattern'.

Note that:

- the patterns are Unix-like. See fnmatch_.
- patterns should be separated by semicolons
- spaces are stripped from the beginning and the end of each pattern
- 'file.js' matches 'file.js' `and` 'file.min.js'

.. warning::
   ``first`` and ``last`` keywords are only available when ``expand=True`` is
   used

Compression
-----------

If you wish to have big_script.dir.js compressed, django-jsdir integrates
without a fuss with django-compressor_. In production, the script gets
compressed like any other js file. Simply use::

    {% compress %}
        {% jsdir 'big_script' %}
    {% endcompress %}


Settings
--------

JSDIR_JSURL
    The default url to access the javascript files directory, relative to the
    static files root. By default it is ``'js'``

.. |copyright| unicode:: 0xA9
.. _django-compressor: http://django-compressor.readthedocs.org/en/latest/
.. _fnmatch: https://docs.python.org/2/library/fnmatch.html
