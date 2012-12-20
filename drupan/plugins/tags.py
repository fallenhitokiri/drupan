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

    def add_tag(self, tag):
        """create tag if it does not exist"""
        if not tag in self.tags:
            self.tags[tag] = []

    def add_object(self, cobj):
        """add object to tag list"""
        for tag in cobj.meta['tags']:
            self.add_tag(tag)
            self.tags[tag].append(cobj)

    def run(self):
        """run the plugin"""
        for cobj in self.site.content:
            if "tags" in cobj.meta:
                self.add_object(cobj)

        for name in self.tags:
            cobj = ContentObject()
            title = name
            menu = False
            cobj.add_meta(title, 'tags', menu)
            cobj.tags = self.tags[name]
            prepare(cobj, self.site)
            self.site.content.append(cobj)
            self.site.tags[name] = cobj.url
