# -*- coding: utf-8 -*-

import yaml

from drupan import fshelpers


def prepare_url(url):
    """make sure URLs end with a '/' and do not start with one"""
    if url[-1:] is not "/":
        url = url + "/"
    if url[:1] is "/":
        url = url[1:]
    return url


class Configuration(object):
    """Read configuration and make sure sane values are returned"""
    def __init__(self, path):
        self.path = fshelpers.ensure_separator(path)
        self.config = yaml.load(fshelpers.read(path, "config.yaml"))

    @property
    def name(self):
        """return name"""
        return self.config['name']

    @property
    def url(self):
        """return URL"""
        url = prepare_url(self.config['url'])
        return url

    @property
    def plugins(self):
        """return list of plugins"""
        return self.config['plugins']

    @property
    def layouts(self):
        """return layouts"""
        for key in self.config['layouts']:
            url = prepare_url(self.config['layouts'][key][0])
            self.config['layouts'][key][0] = url

        return self.config['layouts']

    @property
    def input(self):
        """return input directory"""
        return self.path + fshelpers.ensure_separator(self.config['input'])

    @property
    def template(self):
        """return template directory"""
        return self.path + fshelpers.ensure_separator(self.config['template'])

    @property
    def output(self):
        """return output directory"""
        return self.path + fshelpers.ensure_separator(self.config['output'])

    def options_for_key(self, key):
        """check if a key is in options dictionary and return it.
        Else return False
        """
        # if there are no options self.config['options'] is not iterable
        if not type(self.config['options']) is dict:
            return False

        if key in self.config['options']:
            return self.config['options'][key]
        return False
