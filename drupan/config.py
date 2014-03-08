# -*- coding: utf-8 -*-

"""
drupan.config

Configuration object for drupan. Currently supports file based configuration.
"""

import io

import yaml


class Config(object):
    def __init__(self, options):
        """
        init a new configuration instanze.

        Arguments:
            options: dictionary containing everything necessary to get the
                     configuration from the source (dictionary)
        """
        self.formats = ("yaml")
        self.options = options

        self.raw = None

        if not "type" in options:
            return

        typ = options["type"]

        if typ == "file":
            self.from_file()

    def from_file(self):
        """read configuration from a file"""
        if not "cfg" in self.options:
            raise Exception("Could not find configuration file in options")

        inp = self.options["cfg"]
        with io.open(inp, "r", encoding="utf-8") as source:
            self.raw = source.read()

        self._parse_config()

    def parse_config(self):
        """parse the read configuration"""
        format = self.options.get("format", "yaml")

        if not format in self.formats:
            raise Exception("invalid configuration format")

        if format == "yaml":
            self._parse_yaml()

    def parse_yaml(self):
        """parse yaml configuration and store as attributes"""
        parsed = yaml.load(self.raw)

        # set each key as attribute with the value of the dict
        for key in parsed:
            setattr(self, key, parsed[key])

    def get(self, key):
        """
        Returns:
            value for configuration key
        """
        if not hasattr(self, key):
            message = "could not find key: {0} in config".format(key)
            raise Exception(message)

        return getattr(self, key)
