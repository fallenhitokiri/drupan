# -*- coding: utf-8 -*-

import yaml


class Content(object):
    """Content object"""
    def __init__(self, raw):
        """
        initalize object
        <- raw - content from file
        """
        (header, seperator, content) = raw.partition('---')
        
        meta = yaml.load(header)
        
        self.title   = meta['title']
        self.date    = meta['date']
        self.layout  = meta['layout']
        self.userdef = meta['userdef']
        self.content = content
