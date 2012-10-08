# -*- coding: utf-8 -*-

"""
Zenbo configuration store. Provide sane defaults and add some
sanity checks to the configuration file.
"""

import os
import codecs
import yaml


class Configuration(object):
    def __init__(self, path):
        self.path = path
        cfg_path = path + os.sep + "config.yaml"
        cfg = codecs.open(cfg_path, 'r')
        self.config = yaml.load(cfg)
        cfg.close()

    @property
    def name(self):
        return self.config['name']

    @property
    def url(self):
        url = self.config['url']

        # make sure the base URL always ends with a '/'
        if url[-1:] is not "/":
            url = url + "/"

        return url

    @property
    def plugins(self):
        return self.config['plugins']

    @property
    def layouts(self):
        # make sure URLs end with a '/' and do not start with one
        for key in self.config['layouts']:
            url = self.config['layouts'][key][0]

            if url[-1:] is not "/":
                url = url + "/"
            if url[:1] is "/":
                url = url[1:]

            self.config['layouts'][key][0] = url

        return self.config['layouts']

    def _ensure_separator(self, directory):
        """make sure path ends on os.sep"""
        if directory[-1:] is not os.sep:
            directory = directory + os.sep
        return directory

    @property
    def input(self):
        return self.path + self._ensure_separator(self.config['input'])

    @property
    def template(self):
        return self.path + self._ensure_separator(self.config['template'])

    @property
    def output(self):
        return self.path + self._ensure_separator(self.config['output'])

    def options_for_key(self, key):
        if key in self.config['options']:
            return self.config['options'][key]
        return False
