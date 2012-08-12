# -*- coding: utf-8 -*-

"""
Site object stores everything needed to generate and deploy your site
"""

import os
import codecs

import yaml


class Site(object):
    def __init__(self):
        self.path = None
        self.no_deployment = False
        self.config = None
        self.content = []

    def read_config(self):
        full_path = self.path + os.sep + "config.yaml"
        cfg = codecs.open(full_path, 'r')
        config = yaml.load(cfg)
        cfg.close()

        self.config = config

        # make sure default variables are fine
        # path should end with os seperator
        if self.path[-1:] is not os.sep:
            self.path = self.path + os.sep

        # base URL should always end with a /
        if self.config['url'][-1:] is not "/":
            self.config['url'] = self.config['url'] + "/"
