# -*- coding: utf-8 -*-

"""generate tags
- add a layout to your configuration file
- add a 'tags' array to every content object that should be tagged
"""

from drupan.contentobject import ContentObject
from drupan.url import prepare


class Feature(object):
    """generate tags for each object and create a content object if needed"""
    def __init__(self, site):
        self.site = site
        self.site.tags = {}
        self.tags = {}

    def run(self):
        """run the plugin"""
        for current in self.site.content:
            if "tags" in current.meta:
                for tag in current.meta['tags']:
                    if not tag in self.tags:
                        self.tags[tag] = []
                    self.tags[tag].append(current)

        for name in self.tags:
            cobj = ContentObject()
            title = name
            menu = False
            cobj.add_meta(title, 'tags', menu)
            cobj.tags = self.tags[name]
            prepare(cobj, self.site)
            self.site.content.append(cobj)
            self.site.tags[name] = cobj.url
