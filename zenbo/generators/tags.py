# -*- coding: utf-8 -*-

"""
generate tags

meta informations in posts need an array with tags.

add "tags" to your layouts.
"""

from ..contentobject import ContentObject


class Generator(object):
    def __init__(self, site):
        self.site = site
        self.tags = {}

    def generate(self):
        for current in self.site.content:
            if current.meta.has_key('tags'):
                for tag in current.meta['tags']:
                    if not self.tags.has_key(tag):
                        self.tags[tag] = []
                    self.tags[tag].append(current)

        for name in self.tags:
            co = ContentObject()
            title = name
            menu = False
            co.add_meta(title, 'tags', menu)
            co.tags = self.tags[name]
            self.site.content.append(co)
