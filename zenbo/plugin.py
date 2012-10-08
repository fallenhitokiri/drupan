# -*- coding: utf-8 -*-

"""
return plugin object
"""

# TODO: research if importlib would be an option // Python 2.7 only


class Plugin(object):
    def __init__(self, site):
        self.plugins = []
        self.site = site
        self.load()

    def load(self):
        for name in self.site.config.plugins:
            mod = __import__('zenbo.plugins.%s' % name, fromlist=['Feature'])
            plugin = mod.Feature(self.site)
            self.plugins.append(plugin)
