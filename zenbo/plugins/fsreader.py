# -*- coding: utf-8 -*-

"""
load content from filesystem

configuration:
  - add 'directory' to the input section pointing to the directory that holds
    your content files
  - add 'extension' to the input section specifiying the file extension of your
    content files

requires:
  - pyyaml
"""

import os
import codecs

import yaml

from ..contentobject import ContentObject
from ..url import prepare


class Feature(object):
    def __init__(self, site):
        self.site = site
        self.options = site.config.options_for_key('fsreader')
        self.content_directory = site.config.input
        self.extension = self.options['extension']

        # ensure os seperator
        if self.content_directory[-1:] is not os.sep:
            self.content_directory = self.content_directory + os.sep

    def filelist(self):
        files = []

        for cFile in os.listdir(self.content_directory):
            if self.extension is not None:
                if os.path.splitext(cFile)[1] == self.extension:
                    files.append(cFile)

        return files

    def parse_yaml(self, raw):
        (header, seperator, content) = raw.partition("---")
        meta = yaml.load(header)
        return (meta, content)

    def run(self):
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
