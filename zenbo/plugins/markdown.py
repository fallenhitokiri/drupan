# -*- coding: utf-8 -*-

"""
Convert markdown text to html
"""

from markdown2 import markdown


class Feature(object):
    def __init__(self, site):
        self.site = site

    def run(self):
        for co in self.site.content:
            if co.content is not None:
                co.markup = markdown(co.content)
