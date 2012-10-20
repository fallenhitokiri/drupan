# -*- coding: utf-8 -*-

"""Generate blank content objects
options:
- blank:
    layout1: ['name', in_menu]
    layout2: ['name', in_menu]
in_menu is either True or False
"""

from drupan.contentobject import ContentObject
from drupan.url import prepare


class Feature(object):
    """generate blank content objects"""
    def __init__(self, site):
        self.site = site
        self.options = site.config.options_for_key("blank")
        self.generate = {
            'index': ["Index", False],
            'archive': ["Archive", True],
            'feed': ["Feed", False],
        }

        if self.options:
            self.generate = self.options

    def run(self):
        """run the plugin"""
        for current in self.generate:
            co = ContentObject()
            title = self.generate[current][0]
            menu = self.generate[current][1]
            co.add_meta(title, current, menu)
            prepare(co, self.site)
            self.site.content.append(co)
