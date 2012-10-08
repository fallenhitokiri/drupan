# -*- coding: utf-8 -*-

import argparse

from zenbo.site import Site
from zenbo.plugin import Plugin
from zenbo.serve import Server


class Zenbo(object):
    """Zenbos engine - everything happens here"""
    def __init__(self):
        """parse arguments and create site object"""
        parser = argparse.ArgumentParser(description=Zenbo)
        parser.add_argument('path', help='path to configuration file')
        parser.add_argument('--nodeploy', help='do not deploy',
                             action='store_true', default=False)
        parser.add_argument('--serve', help='serve site',
                             action='store_true', default=False)
        args = parser.parse_args()

        self.site = Site()
        self.site.path = vars(args)['path']
        self.no_deployment = vars(args)['nodeploy']
        self.serve = vars(args)['serve']

    def run(self):
        """run zenbo
        - setup site object
        - load plugins
        - run plugins
        - maybe serve site
        """
        self.site.setup()
        plugins = Plugin(self.site)

        for plugin in plugins.plugins:
            plugin.run()

        if self.serve is True:
            server = Server(self.site)
            server.serve()
