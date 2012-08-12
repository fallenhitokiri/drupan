# -*- coding: utf-8 -*-

"""
create a subset of ContentObjects and sort them

configuration:
  sorting = ['bla', 'foo', 'bar']
"""


class Generator(object):
    def __init__(self, site):
        self.keys = site.config['sorting']
        self.site = site
        self.site.sorted = []

    def generate(self):
        for co in self.site.content:
            if co.meta['layout'] in self.keys:
                self.site.sorted.append(co)

        self.site.sorted.sort(key=lambda co: co.meta['date'])
        self.site.sorted.reverse()
