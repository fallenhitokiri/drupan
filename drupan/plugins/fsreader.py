# -*- coding: utf-8 -*-

"""Load content from filesystem
options:
- fsreader: "file extension used for content"
"""

import yaml

from drupan.contentobject import ContentObject
from drupan.url import prepare
from drupan import fshelpers


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

    def parse_yaml(self, raw):
        """split file and parse yaml header"""
        (header, seperator, content) = raw.partition("---")
        meta = yaml.load(header)
        return (meta, content)

    def run(self):
        """run the plugin"""
        files = fshelpers.filelist(self.content_directory, self.extension)

        # for every file: read, create ContentObject, parse yaml, store
        for current in files:
            raw = fshelpers.read(self.content_directory, current)

            co = ContentObject()
            (co.meta, co.content) = self.parse_yaml(raw)
            prepare(co, self.site)
            self.site.content.append(co)
