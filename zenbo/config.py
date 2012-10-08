# -*- coding: utf-8 -*-

import os
import codecs
import yaml


def ensure_separator(directory):
    """path should end on os.sep"""
    if directory[-1:] is not os.sep:
        directory = directory + os.sep
    return directory


class Configuration(object):
    """Read configuration and make sure sane values are returned"""
    def __init__(self, path):
        self.path = path
        cfg_path = path + os.sep + "config.yaml"
        cfg = codecs.open(cfg_path, 'r')
        self.config = yaml.load(cfg)
        cfg.close()

    @property
    def name(self):
        """return name"""
        return self.config['name']

    @property
    def url(self):
        """return URL"""
        url = self.config['url']

        # make sure the base URL always ends with a '/'
        if url[-1:] is not "/":
            url = url + "/"

        return url

    @property
    def plugins(self):
        """return list of plugins"""
        return self.config['plugins']

    @property
    def layouts(self):
        """return layouts"""
        # make sure URLs end with a '/' and do not start with one
        for key in self.config['layouts']:
            url = self.config['layouts'][key][0]

            if url[-1:] is not "/":
                url = url + "/"
            if url[:1] is "/":
                url = url[1:]

            self.config['layouts'][key][0] = url

        return self.config['layouts']

    @property
    def input(self):
        """return input directory"""
        return self.path + ensure_separator(self.config['input'])

    @property
    def template(self):
        """return template directory"""
        return self.path + ensure_separator(self.config['template'])

    @property
    def output(self):
        """return output directory"""
        return self.path + ensure_separator(self.config['output'])

    def options_for_key(self, key):
        """check if a key is in options dictionary and return it.
        Else return False
        """
        if key in self.config['options']:
            return self.config['options'][key]
        return False
