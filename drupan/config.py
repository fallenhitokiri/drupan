# -*- coding: utf-8 -*-
"""
    drupan.config

    Configuration for drupan. You can configure it by passing a dictionary
    with all values, passing a YAML formatted string or a path to a file.
"""

from io import open

import yaml


class Config(object):
    """hold every information needed by the engine and plugins to work"""
    def __init__(self):
        self.reader = None
        self.writer = None
        self.url_scheme = dict()
        self.plugins = None
        self.options = None
        self.deployment = None

    def from_file(self, cfg):
        """
        read the configuration from a  file

        Arguments:
            cfg: full path to configuration file
        """
        with open(cfg, 'r', encoding='utf-8') as infile:
            self.parse_yaml(infile.read())

    def get_option(self, section, key):
        """
        get a configuration option for a section of the system

        Arguments:
            section: plugin name e.x.
            key: option to get

        Returns:
            configuration option
        """
        sec = self.options.get(section, None)

        if not sec:
            message = "{0} improperly configured".format(section)
            raise Exception(message)

        opt = sec.get(key, None)

        if not opt:
            message = "could not find {0} for {1}".format(section, key)
            raise Exception(message)

        return opt

    def parse_yaml(self, raw):
        """
        parse yaml and configure this instance

        Arguments:
            raw: yaml data
        """
        parsed = yaml.load(raw)
        self.from_dict(parsed)

    def from_dict(self, cfg):
        """
        set instance variables form a dictionary

        Arguments:
            cfg: dictionary with configuration options
        """
        self.reader = cfg.get("reader", None)
        self.writer = cfg.get("writer", None)
        self.url_scheme = cfg.get("url_scheme", None)
        self.plugins = cfg.get("plugins", None)
        self.options = cfg.get("options", None)
        self.deployment = cfg.get("deployment", None)
