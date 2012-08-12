# -*- coding: utf-8 -*-

"""
return plugin object
"""

# TODO: research if importlib would be an option // Python 2.7 only


class Plugin(object):
    def __init__(self, site):
        self.site = site

    def get_loader(self):
        name = self.site.config['input']['name']
        mod = __import__('zenbo.loaders.%s' % name, fromlist=['Loader'])
        loader = mod.Loader(self.site)
        return loader

    def get_generator(self, name):
        mod = __import__('zenbo.generators.%s' % name, fromlist=['Generator'])
        generator = mod.Generator(self.site)
        return generator

    def get_converter(self, name):
        mod = __import__('zenbo.converters.%s' % name, fromlist=['Converter'])
        converter = mod.Converter(self.site)
        return converter

    def get_renderer(self):
        name = self.site.config['rendering']['name']
        mod = __import__('zenbo.rendering.%s' % name, fromlist=['Renderer'])
        renderer = mod.Renderer(self.site)
        return renderer

    def get_writer(self):
        name = self.site.config['output']['name']
        mod = __import__('zenbo.writers.%s' % name, fromlist=['Writer'])
        writer = mod.Writer(self.site)
        return writer

    def get_finalizer(self, name):
        mod = __import__('zenbo.finalizers.%s' % name, fromlist=['Finalizer'])
        finalizer = mod.Finalizer(self.site)
        return finalizer

    def get_deploy(self):
        name = self.site.config['deploy']['name']
        mod = __import__('zenbo.deployment.%s' % name, fromlist=['Deployment'])
        deploy = mod.Deployment(self.site)
        return deploy
