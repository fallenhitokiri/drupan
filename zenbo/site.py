# -*- coding: utf-8 -*-

"""
Site object stores everything needed to generate and deploy your site
"""

import config
import os


class Site(object):
    def __init__(self):
        self.path = None
        self.no_deployment = False
        self.config = None
        self.content = []

    def setup(self):
        # path should end with os seperator
        if self.path[-1:] is not os.sep:
            self.path = self.path + os.sep

        self.config = config.Configuration(self.path)
