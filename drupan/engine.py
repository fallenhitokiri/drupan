# -*- coding: utf-8 -*-

"""
drupan.engine

core part of drupan holding everything together.
"""

from drupan.config import Config
from drupan import inout
from drupan import plugins
from drupan.site import Site
from drupan.entity import Entity


class Engine(object):
    def __init__(self, options):
        """
        init a new engine

        Arguments:
            options: configuration options (dictionary)
        """
        self.config = Config(options)
        self.site = Site(self.config)

        self.reader = None
        self.writer = None

    def run(self):
        """start generating the site"""
        self.read()
        self.run_plugins()

    def watch(self):
        """
        start watching the input directory and generate the site on file change
        """
        pass

    def read(self):
        """read content and generate entities"""
        self._get_reader()
        read = self.reader.get()
        self.site.entities = Entity.from_list(read)

    def _get_reader(self):
        """configure the reader"""
        typ = self.config.reader

        if not typ:
            raise Exception("reader does not exist")

        cls = getattr(inout, typ)
        self.reader = cls.Reader(self.config)

    def run_plugins(self):
        """run all plugins"""
        for name in self.config.plugins:
            if not name in plugins.plugins:
                message = "Plugin: {0} not found".format(name)
                raise Exception(message)

            cls = getattr(plugins, name)
            plugin = cls.Plugin(self.site)
            plugin.run()
