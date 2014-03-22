# -*- coding: utf-8 -*-
"""
    drupan.io.filesystem

    Filesystem implememnts a filesystem reader and writer. It reads drupans
    content files from the your disk and writes the generated site back to it.
"""

import os
from io import open

import yaml

from drupan.entity import Entity


class Reader(object):
    """
    Implements a filesystem reader parsing drupans standard format. It consists
    of a header with all meta data, separated by three dashs from the content.
    """
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config
        self.directory = config.get_option("reader", "directory")
        self.extension = config.get_option("reader", "extension")

        if not self.extension.startswith("."):
            self.extension = ".{0}".format(self.extension)

    def run(self):
        """read and parse content files"""
        for current in os.listdir(self.directory):
            if not os.path.splitext(current)[1] == self.extension:
                continue

            fqp = os.path.join(self.directory, current)

            with open(fqp, 'r', encoding='utf-8') as infile:
                self.parse_file(infile.read())

    def parse_file(self, raw):
        """
        create an entity from a read file

        Arguments:
            raw: input
        """
        (header, seperator, content) = raw.partition("---")
        meta = yaml.load(header)

        entity = Entity(self.config)
        entity.meta = meta
        entity.raw = content.strip()

        self.site.entities.append(entity)
