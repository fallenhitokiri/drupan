# -*- coding: utf-8 -*-

import os

from zenbo.config import Configuration


class Site(object):
    """Site object stores everything that is needed to generate a site"""
    def __init__(self):
        self.path = None
        self.no_deployment = False
        self.config = None
        self.content = []

    def setup(self):
        """read configuration and prepare object"""
        # path should end with os seperator
        if self.path[-1:] is not os.sep:
            self.path = self.path + os.sep

        self.config = Configuration(self.path)
