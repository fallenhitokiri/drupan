# -*- coding: utf-8 -*-

"""
drupan.plugins.blank

Generate some empty content objects. They can be freely filled by the
templating engine to generate an index file or an archive.
"""

from drupan.entity import Entity


class Plugin(object):
    """generate empty entities"""
    def __init__(self, site):
        self.site = site
        self.configure()

    def configure(self):
        """check that this plugin is configured properly"""
        if not hasattr(self.site.config, "blank"):
            raise Exception("Blank isn't configured properly")

        self.config = self.site.config.blank

        if not "entities" in self.config:
            raise Exception("Blank isn't configured properly")

        self.entities = self.config["entities"]

    def run(self):
        """run the plugin"""
        for meta in self.entities:
            new = Entity("")
            new.meta = meta
            self.site.entities.append(new)
