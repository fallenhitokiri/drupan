# -*- coding: utf-8 -*-

"""
drupan.plugins.markdown

Provide markdown support
"""

from markdown2 import markdown


class Plugin(object):
    """convert the content of an entity to markdown"""
    def __init__(self, site):
        self.site = site

        self.config = None
        self.extras = None

        self.configure()

    def configure(self):
        """check that this is plugin configured properly"""
        self.config = self.site.config.markdown

        if not "extras" in self.config:
            raise Exception("Markdown isn't configured properly")

        self.extras = self.config["extras"]

    def run(self):
        """convert entities content to markdown"""
        for entity in self.site.entities:
            if not entity.raw_content:
                continue

            entity.content = markdown(entity.raw_content, extras=self.extras)
