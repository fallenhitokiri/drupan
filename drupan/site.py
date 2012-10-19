# -*- coding: utf-8 -*-

from drupan.config import Configuration


class Site(object):
    """Site object stores everything that is needed to generate a site"""
    def __init__(self):
        self.path = None
        self.no_deployment = False
        self.config = None
        self.content = []

    def setup(self):
        """read configuration and prepare object"""
        self.config = Configuration(self.path)
