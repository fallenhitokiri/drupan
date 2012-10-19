# -*- coding: utf-8 -*-

from markdown2 import markdown


class Feature(object):
    """Convert markdown text to html"""
    def __init__(self, site):
        self.site = site

    def run(self):
        """run the plugin"""
        for cobj in self.site.content:
            if cobj.content is not None:
                cobj.markup = markdown(cobj.content)
