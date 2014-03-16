# -*- coding: utf-8 -*-
"""
    drupan.entity

    Each page / post / snippet / ... is defined as one entity.
"""


class Entity(object):
    """define an entity and all helper methods"""
    def __init__(self, config):
        self.config = config
