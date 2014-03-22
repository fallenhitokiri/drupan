# -*- coding: utf-8 -*-
"""
    drupan.plugins.markdown

    Plugin that provides markdown conversion using markdown2
"""

from markdown2 import markdown


class Plugin(object):
    """convert entities content to markdown using markdown2"""
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config

        self.extras = config.get_option("markdown", "extras")

    def run(self):
        """run the plugin"""
        for entity in self.site.entities:
            if entity.raw:
                self.convert(entity)

    def convert(self, entitiy):
        """
        convert entity.raw to markdown and save it to entity.content

        Arguments:
            entity: instance of drupan.entity.Entity
        """
        entitiy.content = markdown(entitiy.raw, extras=self.extras)
