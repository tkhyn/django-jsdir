import os
from collections import deque
import threading


from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.finders import find
from django.conf import settings


class JSDir(object):
    """
    A class describing a JS directory and implementing methods to carry out
    operations on it

    :ivar js_tag: an HTML script tag template
    :jsdir_ext: the extension for generated script files
    :finders_usage: a (thread_id, use_finders) dictionary.
                    finders_usage[thread_id] is set to true through the
                    runserver management command
    """

    js_tag = '<script type="text/javascript" src="%s"></script>'
    jsdir_ext = '.dir.js'
    finders_usage = {}

    def __init__(self, path):

        # determine if we should use the staticfiles_storage to determine
        # the file system paths or if we should use the staticfiles finders
        self.use_finders = self.finders_usage.get(
            threading.current_thread().ident, False)

        # extract prefix (= subdir of static directory)
        prefix = getattr(settings, 'JSDIR_JSURL', 'js')
        if prefix:
            path = '%s/%s' % (prefix, path)

        # rel path of the directory % static root
        self.dir_path = path
        # rel path of the generated file % static root
        self.jsd_path = path + self.jsdir_ext

        if self.use_finders:
            self.abs_dir_path = find(path)
            self.abs_jsd_path = find(self.jsd_path)
        else:
            self.abs_dir_path = staticfiles_storage.path(path)
            self.abs_jsd_path = staticfiles_storage.path(self.jsd_path)

        self.expand = settings.DEBUG or self.use_finders

    @classmethod
    def set_use_finders(cls, val=True):
        # enables or not the usage of the staticfiles finders for the current
        # thread
        cls.finders_usage[threading.current_thread().ident] = val

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
        return '\n'.join([(self.js_tag % staticfiles_storage.url(rel_p)) \
                          for rel_p in paths])

    def _get_concat_tag(self):
        """
        Returns the HTML tag for the concatenated file
        """

        if not self.abs_jsd_path or not os.path.exists(self.abs_jsd_path):
            self._concatenate()

        return self.js_tag % staticfiles_storage.url(self.jsd_path)

    def _concatenate(self):
        """
        Concatenates all the elementary scripts in one bigger concatenated
        file
        """
        def get_item(path):
            f = open(path, 'r')
            return f.read()
            f.close()

        big_script = self._walk(get_item)

        out_path = self.abs_jsd_path
        if not out_path:
            out_path = self.abs_dir_path + self.jsdir_ext

        out = open(out_path, 'w')
        out.write(''.join(big_script))
        out.close()

    def _walk(self, get_item):
        """
        Walks in the JS directory, executing action for all the js files
        encountered

        :param action: a function taking the absolute path of the file as sole
                       argument
        :returns: the list of parsed files
        """

        items = []
        fifo = deque([self.abs_dir_path])
        while fifo:
            p = fifo.popleft()
            for x in sorted(os.listdir(p)):
                full_p = os.path.join(p, x)
                if os.path.isdir(full_p):
                    fifo.append(full_p)
                elif x.endswith('.js'):
                    items.append(get_item(full_p))
        return items
