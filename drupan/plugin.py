# -*- coding: utf-8 -*-

# TODO: research if importlib would be an option // Python 2.7 only


class Plugin(object):
    """Plugin system
    load, running is implemented in plugins
    """
    def __init__(self, site):
        self.plugins = []
        self.site = site
        self.load()

    def load(self):
        """load all plugins specified in configuration file"""
        for name in self.site.config.plugins:
            mod = __import__('drupan.plugins.%s' % name, fromlist=['Feature'])
            plugin = mod.Feature(self.site)
            self.plugins.append(plugin)
