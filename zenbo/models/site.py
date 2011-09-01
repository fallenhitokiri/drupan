# -*- coding: utf-8 -*-

import os

import yaml

from io import read
from models import content


class Site(object):
    """Site object"""
    def __init__(self, path):
        """
        seutp Site
        <- path - path to site
        """
        cfg    = read(path, 'config.yaml')
        config = yaml.load(cfg)

        self.name        = config['name']
        self.url         = config['url']
        self.directories = config['directories']
        self.markup      = config['markup']
        self.extension   = config['extension']
        self.generators  = config['generators']
        self.urls        = config['urls']
        self.filters     = config['filters']
        self.highlight   = config['highlight']
        self.deployment  = config['deployment']
        self.userdef     = config['userdef']

        if self.url[-1:] is not '/':
            self.url = self.url + '/'

        self.path = path

        if self.path[-1:] is not os.sep:
            self.path = self.path + os.sep


    def load(self):
        """load content from disc"""
        self.content = {}

        for cFile in os.listdir(self.input):
            if os.path.splitext(cFile)[1] == self.extension:
                obj = content.Content(read(self.input, cFile))
                
                #create key with empty array if key does not exist
                if not self.content.has_key(obj.layout):
                    self.content[obj.layout] = []

                self.content[obj.layout].append(obj)


    def sort(self):
        """sort content arrays by date"""
        for key in self.content:
            self.content[key].sort(key=lambda cur: cur.date)
            self.content[key].reverse()


    @property
    def input(self):
        """return path to input"""
        return "%s%s" % (self.path, self.directories['input'])


    @property
    def output(self):
        """return path to output"""
        return "%s%s" % (self.path, self.directories['output'])


    @property
    def template(self):
        """return path to template"""
        return "%s%s" % (self.path, self.directories['template'])


    def __unicode__(self):
        """return name and url"""
        return "%s - %s" % (self.name, self.url)


    def __str__(self):
        """return name and url"""
        return unicode(self).encode('utf-8')
