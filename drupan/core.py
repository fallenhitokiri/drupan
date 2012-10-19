# -*- coding: utf-8 -*-

import argparse
import sys

from drupan.site import Site
from drupan.plugin import Plugin
from drupan.serve import Server
from drupan.initialize import bootstrap


class Drupan(object):
    """drupan engine - everything happens here"""
    def __init__(self):
        """parse arguments and create site object"""
        parser = argparse.ArgumentParser(description='drupan')
        parser.add_argument('path', help='path to configuration file')
        parser.add_argument('--nodeploy', help='do not deploy',
                             action='store_true', default=False)
        parser.add_argument('--serve', help='serve site',
                             action='store_true', default=False)
        parser.add_argument('--init', help="create new site at path",
                             action='store_true', default=False)
        args = parser.parse_args()

        if not vars(args)['init']:
            self.site = Site()
            self.site.path = vars(args)['path']
            self.no_deployment = vars(args)['nodeploy']
            self.serve = vars(args)['serve']
        else:
            self.initialize(vars(args)['path'])

    def run(self):
        """run denbo
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

    def initialize(self, path):
        """init new site"""
        bootstrap(path)
        sys.exit(0)
