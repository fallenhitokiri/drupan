# -*- coding: utf-8 -*-

"""Load content from filesystem
options:
- fsreader: "file extension used for content"
"""

import os
import codecs

import yaml

from ..contentobject import ContentObject
from ..url import prepare


class Feature(object):
    """load content from filesystem"""
    def __init__(self, site):
        self.site = site
        self.options = site.config.options_for_key('fsreader')
        self.content_directory = site.config.input
        self.extension = '.md'

        if self.options:
            self.extension = self.options
            
            # extension should start with a dot
            if self.extension[0:1] is not '.':
                self.extension = '.' + self.extension

        # ensure os seperator
        if self.content_directory[-1:] is not os.sep:
            self.content_directory = self.content_directory + os.sep

    def filelist(self):
        """list all files in a directory and exclude self.extension"""
        files = []

        for cfile in os.listdir(self.content_directory):
            if self.extension is not None:
                if os.path.splitext(cfile)[1] == self.extension:
                    files.append(cfile)

        return files

    def parse_yaml(self, raw):
        """split file and parse yaml header"""
        (header, seperator, content) = raw.partition("---")
        meta = yaml.load(header)
        return (meta, content)

    def run(self):
        """run the plugin"""
        files = self.filelist()

        # for every file: read, create ContentObject, parse yaml, store
        for current in files:
            full = self.content_directory + current

            cfile = codecs.open(full, 'r', 'utf-8')
            raw = cfile.read()
            cfile.close()

            co = ContentObject()
            (co.meta, co.content) = self.parse_yaml(raw)
            prepare(co, self.site)
            self.site.content.append(co)
