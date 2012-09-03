# -*- coding: utf-8 -*-

"""
Zenbos engine - everything happens here
"""

import argparse

from site import Site
from plugin import Plugin
from serve import Server
import url


class Zenbo(object):
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
        self.site.read_config()
        plugin = Plugin(self.site)

        loader = plugin.get_loader()
        loader.load()

        for generator in self.site.config['generators']:
            gen = plugin.get_generator(generator)
            gen.generate()

        for co in self.site.content:
            url.prepare(co, self.site)

        for converter in self.site.config['converters']:
            conv = plugin.get_converter(converter)
            conv.convert()

        renderer = plugin.get_renderer()
        renderer.render()

        writer = plugin.get_writer()
        writer.write()

        for finalizer in self.site.config['finalizers']:
            fin = plugin.get_finalizer(finalizer)
            fin.finalize()

        if self.no_deployment is False:
            deployer = plugin.get_deploy()
            deployer.deploy()

        if self.serve is True:
            server = Server(self.site)
            server.serve()
