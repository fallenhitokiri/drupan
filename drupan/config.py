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
        self.plugins = list()
        self.options = None
        self.deployment = None
        self.redirects = None
        self.external_plugins = None

    def from_file(self, cfg):
        """
        read the configuration from a  file

        Arguments:
            cfg: full path to configuration file
        """
        with open(cfg, 'r', encoding='utf-8') as infile:
            self.parse_yaml(infile.read())

    def get_option(self, section, key, optional=False):
        """
        get a configuration option for a section of the system

        Arguments:
            section: plugin name e.x.
            key: option to get
            optional: if False an exception will be raised if the key cannot
                      be found.

        Returns:
            configuration option
        """
        # compatibility for 2.0 configuration
        if key == "redirects" and section is None:
            return self.redirects

        sec = self.options.get(section, None)

        if not sec:
            if optional:
                return None

            message = "{0} improperly configured".format(section)
            raise Exception(message)

        opt = sec.get(key, None)

        if not opt:
            if optional:
                return None

            message = "could not find {0} for {1}".format(key, section)
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
        self.redirects = cfg.get("redirects", None)
        self.external_plugins = cfg.get("external_plugins", None)
