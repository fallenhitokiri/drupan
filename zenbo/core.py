# -*- coding: utf-8 -*-

"""Core of Zenbo"""

import argparse

from models import site


class Zenbo(object):
    """Zenbo"""
    def __init__(self):
        """
        setup Zenbo
        - parse command line arguments
        """
        parser = argparse.ArgumentParser(description='Zenbo')
        parser.add_argument('path', help='directory you store your site in')
        args = parser.parse_args()

        self.path= vars(args)['path']


    def run(self):
        """run Zenbo"""
        self._compile()


    def _compile(self):
        """compile site"""
        self.site = site.Site(self.path)
        self.site.load()
        self.site.sort()
