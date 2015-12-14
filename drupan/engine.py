# -*- coding: utf-8 -*-
"""
    drupan.engine

    The engine is part of drupan that holds all plugins and subsystems
    together and runs the actual site creation process.
"""

from .site import Site
from .config import Config
from .template import Render
from .serve import http


class Engine(object):
    """Drupan engine doing all the work"""
    def __init__(self):
        self.site = Site()
        self.config = Config()
        self.reader = None
        self.writer = None
        self.plugins = list()
        self.renderer = None
        self.deployment = None

    def prepare_engine(self):
        """get all subsystems and plugins setup"""
        self.reader = __import__(
            "drupan.inout.{0}".format(self.config.reader),
            fromlist=["Reader"]
        ).Reader(self.site, self.config)

        self.writer = __import__(
            "drupan.inout.{0}".format(self.config.writer),
            fromlist=["Writer"]
        ).Writer(self.site, self.config)

        self._prepare_plugins()

        self.renderer = Render(self.site, self.config)

        if self.config.deployment:
            self.deployment = __import__(
                "drupan.deployment.{0}".format(self.config.deployment),
                fromlist=["Deploy"]
            ).Deploy(self.site, self.config)

    def _prepare_plugins(self):
        """Create an instance of all plugins and add them to self.plugins.

        First try to import the plugin from python path with the package name
        `drupan$name`. If the import fails try to import the plugin from drupan
        standard plugin module.
        """
        for name in self.config.plugins:
            try:
                plugin_name = "drupan{0}".format(name)
                imported = __import__(plugin_name, fromlist=["Plugin"])
            except ImportError:
                plugin_name = "drupan.plugins.{0}".format(name)
                imported = __import__(plugin_name, fromlist=["Plugin"])

            plugin = imported.Plugin(self.site, self.config)
            self.plugins.append(plugin)

    def run(self):
        """run the site generation process"""
        self.reader.run()
        for plugin in self.plugins:
            plugin.run()
        self.renderer.run()
        self.writer.run()

    def serve(self):
        """serve the generated site"""
        http(self.config.get_option("writer", "directory"))

    def deploy(self):
        """deploy the generated site"""
        if not self.deployment:
            return

        self.deployment.run()
