# -*- coding: utf-8 -*-
"""
    drupan.plugins.tags

    Create tag entities for all tagged objects.
"""

from drupan.entity import Entity


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

        self.tags = dict()

    def run(self):
        """run the plugin"""
        for entity in self.site.entities:
            self.generate_tags(entity)

        for tag in self.tags:
            self.site.entities.append(self.tags[tag])

        self.site.tags = self.tags

    def generate_tags(self, entity):
        """
        Generate entities for all tags in an entities meta information

        Arguments:
            instance of drupan.entity.Entity
        """
        if not "tags" in entity.meta:
            return

        for tag in entity.meta["tags"]:
            self.create_entity(tag)
            tag = tag.lower()
            self.tags[tag].entities.append(entity)

    def create_entity(self, tag):
        """
        Create a new entity for a tag if it does not exist

        Arguments:
            tag: tag name
        """
        lower = tag.lower()

        if lower in self.tags:
            return

        entity = Entity(self.config)
        entity.meta["title"] = tag
        entity.meta["layout"] = "tag"
        entity.entities = list()

        self.tags[lower] = entity
