# -*- coding: utf-8 -*-

"""Core of Zenbo"""

import argparse

from models import site
from template import render
from loader import load
from write import write
from deployment import *
from plugins import *


class Zenbo(object):
    """Zenbo"""
    def __init__(self):
        """
        setup Zenbo
        - parse command line arguments
        """
        parser = argparse.ArgumentParser(description='Zenbo')

        parser.add_argument('path', help='directory you store your site in')
        parser.add_argument('--nodeploy', help='do not deploy after generation', action='store_true', default=False)

        args = parser.parse_args()
        
        self.path   = vars(args)['path']
        self.deploy = vars(args)['nodeploy']


    def run(self):
        """run Zenbo"""
        self._compile()

        if self.deploy is True:
            print "Not deploying generated page!"
        else:
            getattr(eval(self.site.deployment['type']), 'publish')(self.site)


    def __plugin(self, step):
        """run all plugins that match the current step"""
        for plugin in self.site.plugins:
            info = getattr(eval(plugin), 'plugin')()

            if info['step'] is step:
                getattr(eval(plugin), 'execute')(self.site)


    def _compile(self):
        """compile site"""
        self.site = site.Site(self.path)
        
        load(self.site)
        self.__plugin("load")
        
        render(self.site)
        self.__plugin("render")

        write(self.site)
        self.__plugin("write")
