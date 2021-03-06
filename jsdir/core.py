import os
import sys
import re
import fnmatch

from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find
from django.conf import settings
from django.utils.six import string_types


js_tag = '<script type="text/javascript" src="%s"></script>'
jsdir_ext = 'dir.js'


class JSDir(object):
    """
    A class describing a JS directory and implementing methods to carry out
    operations on it

    :finders_usage: a (thread_id, use_finders) dictionary.
                    finders_usage[thread_id] is set to true through the
                    runserver management command
    """

    finders_usage = {}

    def __init__(self, path, expand=False, **kwargs):

        if ':' in path.split('/')[0]:
            raise NotImplementedError('jsdir: external urls like %s are not '
                                      'supported' % path)

        # determine if we should use the staticfiles_storage to determine
        # the file system paths or if we should use the staticfiles finders
        self.use_finders = self.finders_usage.get(os.getpid(), False)

        # extract prefix (= subdir of static directory)
        prefix = getattr(settings, 'JSDIR_JSURL', 'js')
        if path.startswith('/'):
            # absolute path, no prefix
            path = path[1:]
        elif prefix:
            # add prefix if any
            path = '%s/%s' % (prefix, path)

        # extract name if any
        name = kwargs.pop('name', None)

        # rel path of the directory % static root
        self.dir_path = path
        # rel path of the generated file % static root
        self.jsd_ext = jsdir_ext
        if name is not None:
            self.jsd_ext = '.'.join((name, jsdir_ext))
        self.jsd_path = '.'.join((path, self.jsd_ext))

        if self.use_finders:
            self.abs_dir_path = find(path)
            self.abs_jsd_path = find(self.jsd_path)
        else:
            self.abs_dir_path = staticfiles_storage.path(path)
            self.abs_jsd_path = staticfiles_storage.path(self.jsd_path)

        self.expand = expand or settings.DEBUG or self.use_finders

        self.include = []
        self.exclude = []
        self.first = []
        self.last = []
        attrs = ['include', 'exclude']
        if self.expand:
            attrs.extend(['first', 'last'])
            self.minify = not settings.DEBUG and expand and \
                          kwargs.get('minify', True)
        else:
            self.minify = False

        for attr in attrs:
            patterns = kwargs.pop(attr, [])
            if isinstance(patterns, string_types):
                patterns = [p.strip() for p in patterns.split(';') if p.strip()]
            for p in patterns:
                getattr(self, attr).append(re.compile(fnmatch.translate(p)))

    @classmethod
    def set_use_finders(cls, val=True):
        # enables or not the usage of the staticfiles finders for the current
        # process id (not thread)
        cls.finders_usage[os.getpid()] = val

    def get_tags(self):
        if self.expand:
            return self._get_expand_tags()
        else:
            # use the concatenated file if it exist,
            # and generate it if it doesn't
            return self._get_concat_tag()

    def _get_expand_tags(self):
        """
        Returns a string with a <script> HTML tag for each js file in the
        JS directory
        """
        if not os.path.isdir(self.abs_dir_path):
            raise ValueError('jsdir: %s is not a directory' %
                             self.abs_dir_path)

        # walks the js directory. We cannot use os.walk as it would break
        # the alphabetic ordering between files and folders
        static_base = self.abs_dir_path.replace(
            os.path.normpath(self.dir_path), '')

        def get_item(path):
            return os.path.relpath(path, static_base).replace('\\', '/')

        paths = self._walk(get_item)
        return '\n'.join([(js_tag % staticfiles_storage.url(rel_p)) \
                          for rel_p in paths])

    def _get_concat_tag(self):
        """
        Returns the HTML tag for the concatenated file
        """

        if not self.abs_jsd_path or not os.path.exists(self.abs_jsd_path):
            self.concatenate()

        return js_tag % staticfiles_storage.url(self.jsd_path)

    def concatenate(self):
        """
        Concatenates all the elementary scripts in one bigger concatenated
        file
        """
        def get_item(path):
            f = open(path, 'r')
            read = f.read()
            f.close()
            return read

        big_script = self._walk(get_item)

        out_path = self.abs_jsd_path
        if not out_path:
            out_path = '.'.join((self.abs_dir_path, self.jsd_ext))

        out = open(out_path, 'w')
        out.write(''.join(big_script))
        out.close()

    def _walk(self, get_item):
        """
        Walks in the JS directory, executing action for all the js files
        encountered

        :param get_item: a function taking the absolute path of the file as
                         sole argument
        :returns: the list of parsed files
        """

        firsts = [[] for f in self.first]
        included = [[] for f in self.include]
        middle = []
        lasts = [[] for l in self.last]

        def append_item(path):
            item = get_item(path)
            split_path = os.path.split(path)
            path = os.path.join(os.path.relpath(split_path[0],
                                                self.abs_dir_path),
                                split_path[-1].replace('.min', ''))
            if sys.platform == 'win32':
                path = path.replace('\\', '/')
            path = path.lstrip('./')

            # first look in included patterns, reject anything that does not
            # match
            include_index = None
            for i, x in enumerate(self.include):
                if x.match(path):
                    include_index = i
                    break
            else:
                if self.include:
                    # rejected file
                    return

            for x in self.exclude:
                if x.match(path):
                    return

            # look in firsts
            for i, x in enumerate(self.first):
                if x.match(path):
                    firsts[i].append(item)
                    return
            # look in lasts
            for i, x in enumerate(self.last):
                if x.match(path):
                    lasts[i].append(item)
                    return
            # not found, append in the middle if include_index is not there
            if include_index is not None:
                included[include_index].append(item)
            else:
                middle.append(item)

        def walk(path):
            for x in sorted(os.listdir(path)):
                full_p = os.path.join(path, x)
                if os.path.isdir(full_p):
                    walk(full_p)
                elif x.endswith('.js'):
                    minified = x.endswith('.min.js')
                    if self.minify:
                        # we are in expand + minified mode, look for minified
                        # files only
                        if not minified:
                            continue
                    elif minified:
                        # we are in concat or non-minified mode,
                        # ignore minified files
                        continue
                    append_item(full_p)

        walk(self.abs_dir_path)

        # concatenates the lists
        result = []
        for l in firsts + included:
            result.extend(l)
        result.extend(middle)
        for l in reversed(lasts):
            result.extend(l)

        return result
