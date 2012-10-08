# -*- coding: utf-8 -*-

"""
generate tags

meta informations in posts need an array with tags.

add "tags" to your layouts.
"""

from ..contentobject import ContentObject
from ..url import prepare


class Feature(object):
    def __init__(self, site):
        self.site = site
        self.tags = {}

    def run(self):
        for current in self.site.content:
            if "tags" in current.meta:
                for tag in current.meta['tags']:
                    if not tag in self.tags:
                        self.tags[tag] = []
                    self.tags[tag].append(current)

        for name in self.tags:
            co = ContentObject()
            title = name
            menu = False
            co.add_meta(title, 'tags', menu)
            co.tags = self.tags[name]
            prepare(co, self.site)
            self.site.content.append(co)
