# -*- coding: utf-8 -*-


class Plugin(object):
    def __init__(self, site, config):
        self.site = site
        self.config = config
        self.ran = False
        self.name = "TestPlugin"

    def run(self):
        self.ran = True
