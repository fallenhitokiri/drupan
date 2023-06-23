# -*- coding: utf-8 -*-
"""
    drupan.engine

    The engine is part of drupan that holds all plugins and subsystems
    together and runs the actual site creation process.
"""
import enum
import os
import sys
from contextvars import ContextVar

from .site import Site
from .config import Config
from .template import Render
from .serve import HTTPServer


class EngineStateVerbs(enum.Enum):
    setting_up_engine = "setting up engine"


class Engine(object):
    """Drupan engine doing all the work"""
    var: ContextVar[int] = ContextVar('var', default=42)

    def __init__(self, engine_name=None, **kwargs):
        self.engine_name = engine_name or 'drupan'
        self.site = Site()
        self.config = Config()
        self.reader = None
        self.writer = None
        self.plugins = list()
        self.plugins_run_first = list()
        self.renderer = None
        self.deployment = None
        self.logger = None
        self.run_after = []
        self.context = {
            'current_verb': 'setting up engine',
            'subjects': {

            }

        }
        self.subjects = {

        }

    def get_state_str(self, name, state):
        return f"""{name}:\n state: {state}\n"""

    def context_info(self):
        info = ""
        info += self.get_state_str('Engine', self.context['current_verb'])
        for k, v in self.context['subjects'].items():
            info += self.get_state_str(k, v)
        return info

    def set_verb(self, what):
        self.context['current_verb'] = what

    def update_context(self, name, state):
        # print(f"Engine got update from {name} state is {state}")
        self.subjects[name] = state

    def prepare_engine(self):
        """get all subsystems and plugins setup"""
        self.set_verb('adding plugins')
        self.add_external_plugins()

        if self.config.reader:
            imported = self._load_module(self.config.reader, "inout", "Reader")
            self.reader = imported.Reader(self.site, self.config)

        if self.config.writer:
            imported = self._load_module(self.config.writer, "inout", "Writer")
            self.writer = imported.Writer(self.site, self.config)

        for name in self.config.plugins:
            self.set_verb(f'loading plugin {name}')
            imported = self._load_module(name, "plugins", "Plugin", engine_name=self.engine_name)
            plugin = imported.Plugin(self.site, self.config)
            if hasattr(plugin, "run_first"):
                self.plugins_run_first.append(plugin)
            else:
                self.plugins.append(plugin)
            if hasattr(plugin, "run_after"):
                self.run_after.append({
                    'plugin': plugin,
                    'func': getattr(plugin, "run_after")
                })

        self.renderer = Render(self.site, self.config)
        self.renderer.attach(self)
        self.site.attach(self)

        if self.config.deployment:
            print("deployment is on")
            imported = self._load_module(
                self.config.deployment,
                "deployment",
                "Deploy",
            )
            self.deployment = imported.Deploy(self.site, self.config)

        self.logger = self.config.logger

    @staticmethod
    def _load_module(name, base_name, kind, *args, **kwargs):
        """Load a drupan module and return it. First try to load a module from
        path with the format `drupan-$pluginName` before trying to import a
        plugin from the drupan distribution.

        If both imports fail let drupan run into an ImportError exception since
        something is clearly broken.

        :param name: name of the module to load
        :param base_name: base path for drupan standard module
        :param kind: class to import
        :returns: imported class from `name`
        """
        engine_name = kwargs.get("engine_name", "drupan")
        try:
            plugin_name = "drupan-{0}".format(name)
            return __import__(plugin_name, fromlist=[kind])
        except ImportError:
            try:
                plugin_name = f"{engine_name}-{name}"
                return __import__(plugin_name, fromlist=[kind])
            except ImportError:
                plugin_name = "drupan.{0}.{1}".format(base_name, name)
                return __import__(plugin_name, fromlist=[kind])

    def add_external_plugins(self):
        """Add external plugin path to Python path."""
        if not self.config.external_plugins:
            return

        plugin_path = self.config.external_plugins
        print(f"Loading from {self.config.external_plugins}")

        if not os.path.exists(plugin_path):
            raise Exception("External plugin path does not exist.")

        sys.path.append(plugin_path)

    def run(self):
        self.plugins = list(set(self.plugins))
        self.plugins_run_first = list(set(self.plugins_run_first))
        """run the site generation process"""
        if self.reader:
            self.set_verb("running reader")
            self.reader.run()

        for plugin in self.plugins:
            self.set_verb(f"running plugin {plugin}")
            plugin.run()
        self.set_verb("running render")
        self.renderer.run()
        self.set_verb("running writer")

        for plugin in self.plugins_run_first:
            self.set_verb(f"running plugin {plugin}")
            plugin.run()

        print("writing")

        if self.writer:
            print("started")
            self.writer.run()

        for p in self.run_after:
            plug = p['plugin']
            f = getattr(plug, p['func'])
            f()

        if self.deployment:
            self.deployment.run()

        # self.logger.close()

    def serve(self):
        """serve the generated site"""
        server = HTTPServer(self.config)
        server.serve()
