# -*- coding: utf-8 -*-
"""
    drupan.entity

    Each page / post / snippet / ... is defined as one entity.
"""


class Entity(object):
    """define an entity and all helper methods"""
    def __init__(self, config):
        self.config = config

        self.meta = dict()
        self.raw = None
        self.content = None

    @property
    def layout(self):
        """
        Returns:
            layout for this entity
        """
        return self.meta["layout"]
