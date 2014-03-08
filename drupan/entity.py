# -*- coding: utf-8 -*-

"""
drupan.entity

Content object storing everything related to an entity.
"""

import yaml


class Entity(object):
    """define an entity - each object read or generated"""
    def __init__(self, raw):
        self.raw = raw

        self.raw_meta = None
        self.raw_content = None
        self.meta = None

        # attributes used by plugins
        self.content = None
        self.rendered = None

    @classmethod
    def from_list(cls, content):
        """
        Create new entities from a list

        Arguments:
            content: list of read content

        Returns:
            list with new entities
        """
        entities = []

        for raw in content:
            entity = cls(raw)
            entity.from_yaml()
            entities.append(entity)

        return entities

    def from_yaml(self):
        """assume that raw is a yaml document and prepare this entity"""
        self.split()
        self.parse_yaml()

    def split(self):
        """split raw content into meta data and content"""
        (meta, seperator, content) = self.raw.partition("---")
        self.raw_meta = meta
        self.raw_content = content

    def parse_yaml(self):
        """parse raw meta data using yaml"""
        self.meta = yaml.load(self.raw_meta)

