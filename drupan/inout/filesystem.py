# -*- coding: utf-8 -*-
"""
    drupan.io.filesystem

    Filesystem implememnts a filesystem reader and writer. It reads drupans
    content files from the your disk and writes the generated site back to it.
"""

import os
from io import open
import shutil
import errno
from HTMLParser import HTMLParser

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


class Writer(object):
    """
    Implements a filesystem writer, writing all entities which have a rendered
    attribute != None. The path is the URL split and appended to the base path.
    """
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config

        self.base_path = config.get_option("writer", "directory")
        self.template = config.get_option("jinja", "template")

    def run(self):
        """run the plugin"""
        self.cleandir()
        self.copytree()

        for entity in self.site.entities:
            self.create_path(entity)
            self.write(entity)
            self.copy_images(entity)

    def cleandir(self):
        """clean the output directory"""
        try:
            shutil.rmtree(self.base_path)
        except:
            pass

    def copytree(self):
        """
        copy the template directory to the output directory, skip files
        prefixed with _
        """
        ignore = shutil.ignore_patterns("_*")
        shutil.copytree(self.template, self.base_path, ignore=ignore)

    def create_path(self, entity):
        """
        Create all directories needed to write an entity.

        Arguments:
            entity: entity to write (drupan.entity.Entity)
        """
        if entity.path == "":
            return

        path = os.path.join(self.base_path, entity.path)

        if os.path.exists(path):
            return

        try:
            os.makedirs(path)
        except OSError:
            if OSError.errno == errno.EEXIST:
                pass
            else:
                raise

    def write(self, entity):
        """
        Write an entity to disk

        Arguments:
            entity: entity to write (drupan.entity.Entity)
        """
        path = os.path.join(self.base_path, entity.path, "index.html")

        with open(path, "w", encoding="utf-8") as output:
            output.write(entity.rendered)

    def copy_images(self, entity):
        """
        Copy images that are linked in this entity to the entity folder

        Arguments:
            entity: entity to copy images to
        """
        if entity.rendered is None:
            return

        parser = ImageParser()
        parser.feed(entity.rendered)

        # no images found?
        if len(parser.images) == 0:
            return

        path = os.path.join(self.base_path, entity.path)
        source = os.path.join(
            self.config.get_option("reader", "directory"),
            "images"
        )

        for linked in parser.images:
            origin = os.path.join(source, linked)
            shutil.copy(origin, path)


class ImageParser(HTMLParser):
    """Handler based on HTMLParser for images"""
    def __init__(self):
        self.images = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """if image tag is found add it to self.images"""
        if tag == 'img':
            self.images.append((dict(attrs)['src']))
