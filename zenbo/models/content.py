# -*- coding: utf-8 -*-

import yaml

from io import read


class Content(object):
    """Content object"""
    def fromFile(self, path, name):
        """
        parse content from files
        <- path: path to file
           name: filename
        """
        raw = read(path, name)

        (header, seperator, content) = raw.partition('---')
        
        meta = yaml.load(header)
        
        self.title   = meta['title']
        self.date    = meta['date']
        self.layout  = meta['layout']
        self.userdef = meta['userdef']
        self.content = content
