# -*- coding: utf-8 -*-


class Site(object):
    """define the site model holding everything together"""
    def __init__(self, config):
        self.config = config
        self.entities = None
