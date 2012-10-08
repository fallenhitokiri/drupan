# -*- coding: utf-8 -*-

"""
create a subset of ContentObjects and sort them

configuration:
  sorting = ['bla', 'foo', 'bar']
"""


class Feature(object):
    def __init__(self, site):
        self.site = site
        self.site.sorted = []
        self.options = site.config.options_for_key('sorting')

    def run(self):
        for co in self.site.content:
            if co.meta['layout'] in self.options:
                self.site.sorted.append(co)

        self.site.sorted.sort(key=lambda co: co.meta['date'])
        self.site.sorted.reverse()
