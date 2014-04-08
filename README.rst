django-jsdir
============

|copyright| 2014 Thomas Khyn, MIT License

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


Setup
-----

1. Install using your prefered method
2. Add ``'jsdir'`` to your INSTALLED_APPS
3. If you are using Jinja2, add ``'jsdir.jjext'`` to your Jinja2 extensions
   list


How it works
------------

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

1. linking all the scripts nested under big_script.js directory tree when in
   development mode with files served from the application's static directory.
   This will change nothing from the developer's point of view, except he won't
   need to update the script list anymore
2. concatenating (and possibly compressing, with the help of
   django-compressor_) all the nested subscripts in one file named
   `big_script.js` when you'll run ``manage.py collectstatic``
3. linking the generated `big_script.js` when in production mode

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


Compression
-----------

If you wish to have your big_script.js compressed, django-jsdir integrates
without a fuss with django-compressor_. The big_script.js can get compressed as
any other js file. Simply use::

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
