# -*- coding: utf-8 -*-

"""Core of Zenbo"""

import argparse

from models import site
from template import render
from loader import load
from generator import generate
from write import write
from deploy import deploy


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
            print "deploying,..."
            deploy(self.site)


    def _compile(self):
        """compile site"""
        self.site = site.Site(self.path)
        load(self.site)
        self.site.sort()
        generate(self.site)
        render(self.site)
        write(self.site)
        
