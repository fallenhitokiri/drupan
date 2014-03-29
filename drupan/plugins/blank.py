# -*- coding: utf-8 -*-
"""
    drupan.plugins.blank

    Generate empty entities to be used for something that does not require
    its own content file.
"""

from drupan.entity import Entity


class Plugin(object):
    """create empty entities"""
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config

        self.generate = config.get_option("blank", "generate")

    def run(self):
        """run the plugin"""
        for name in self.generate:
            new = Entity(self.config)
            new.meta["title"] = name
            new.meta["layout"] = self.generate[name]
            self.site.entities.append(new)
