# -*- coding: utf-8 -*-

import sys

from drupan.site import Site
from drupan.plugin import Plugin
from drupan.serve import Server
from drupan.initialize import bootstrap


class Drupan(object):
    """drupan engine - everything happens here"""
    def setup(self, path, nodeploy, serve):
        """setup engine"""
        self.site = Site()
        self.site.path = path
        self.no_deployment = nodeploy
        self.serve = serve

    def run(self):
        """run drupan"""
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
