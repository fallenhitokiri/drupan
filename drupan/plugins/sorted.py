# -*- coding: utf-8 -*-

"""sort content objects
- add to your configuration file:
    sorting = ['layout1', 'layout2', 'layout3']
"""


class Feature(object):
    """create a subset of ContentObjects and sort them"""
    def __init__(self, site):
        self.site = site
        self.site.sorted = []
        self.options = site.config.options_for_key('sorting')

    def run(self):
        """run the plugin"""
        for cobj in self.site.content:
            if cobj.meta['layout'] in self.options:
                self.site.sorted.append(cobj)

        self.site.sorted.sort(key=lambda cobj: cobj.meta['date'])
        self.site.sorted.reverse()
