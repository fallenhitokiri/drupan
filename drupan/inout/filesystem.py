# -*- coding: utf-8 -*-
"""
    drupan.io.filesystem

    Filesystem implements a filesystem reader and writer. It reads drupans
    content files from the your disk and writes the generated site back to it.
"""

import os
from io import open
import shutil
import errno
import re

import yaml

from drupan.entity import Entity
from drupan.file_wrapper import FileWrapper


class Reader(object):
    """
    Implements a filesystem reader parsing drupans standard format. It consists
    of a header with all meta data, separated by three dashes from the content.
    """
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config
        self.content = config.get_option("reader", "content", optional=True)
        self.extension = config.get_option("reader", "extension")
        self.template = config.get_option("reader", "template", optional=True)

        if self.content is None:
            # Try getting the content directory via the content key. This
            # preserves 2.0 config format. Will be removed in 3.0
            self.content = config.get_option("reader", "directory")
            print("Please rename your directory key to content.")

        if self.template is None:
            # If the reader is not configured for templates try getting it
            # via the jinja key. This preserves the behavior of the 2.0 config
            # format. Will be removed in 3.0
            self.template = config.get_option("jinja", "template")
            print("Please move your template key to the reader section.")

        if not self.extension.startswith("."):
            self.extension = ".{0}".format(self.extension)

    def run(self):
        """read and parse all files"""
        self.read_content()
        self.read_template()
        self.read_images()

    def read_content(self):
        """read the content files and create entities"""
        for current in os.listdir(self.content):
            if not os.path.splitext(current)[1] == self.extension:
                continue

            fqp = os.path.join(self.content, current)

            with open(fqp, 'r', encoding='utf-8') as infile:
                self.parse_file(infile.read())

    def parse_file(self, raw):
        """
        create an entity from a read file

        Arguments:
            raw: input
        """
        (header, separator, content) = raw.partition("---")
        meta = yaml.load(header)

        entity = Entity(self.config)
        entity.meta = meta
        entity.raw = content.strip()

        self.site.entities.append(entity)

    def read_template(self):
        """read template files and populate template dict"""
        template_extensions = (".html", ".htm", ".xml", ".txt")

        for file_names, dir_name in dir_walker(self.template):
            for name in file_names:
                if name.startswith("."):
                    continue

                store = self.site.templates
                mode = "r"

                if not name.endswith(template_extensions):
                    store = self.site.assets
                    mode = "rb"

                # remove template dir part from directory name
                stripped = re.sub(self.template, "", dir_name)

                # remove leading separator if exists
                if stripped.startswith(os.path.sep):
                    stripped = stripped[1:]

                fqp = os.path.join(dir_name, name)
                key = os.path.join(stripped, name)

                if name.endswith(template_extensions):
                    with open(fqp, mode) as infile:
                        store[key] = infile.read()
                else:
                    store[key] = FileSystemFileWrapper(fqp)

    def read_images(self):
        """read images and populate images dict"""
        path = os.path.join(self.content, "images")

        for file_names, dir_name in dir_walker(path):
            for name in file_names:
                if name.startswith("."):
                    continue

                fqp = os.path.join(dir_name, name)
                self.site.images[name] = FileSystemFileWrapper(fqp)


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

    def run(self):
        """run the plugin"""
        self.clean_dir()
        self.write_entities()
        self.write_assets()
        self.write_templates()

    def write_entities(self):
        """write entities to files"""
        for entity in self.site.entities:
            if entity.path is None:
                continue

            path = os.path.join(self.base_path, entity.path)
            create_path(path)

            path = os.path.join(path, "index.html")
            write(entity.rendered, path)

            self.write_images(entity)

    def write_assets(self):
        """write assets to files"""
        for name, content in self.site.assets.items():
            path = os.path.join(self.base_path, os.path.dirname(name))
            create_path(path)

            path = os.path.join(self.base_path, name)
            write(content, path)

    def write_templates(self):
        """write template files which are not prefixed with _"""
        for name, content in self.site.templates.items():
            if name.startswith("_"):
                continue

            path = os.path.join(self.base_path, os.path.dirname(name))
            create_path(path)

            path = os.path.join(self.base_path, name)
            write(content, path)

    def write_images(self, entity):
        """
        Write images that are linked in this entity to the entity folder

        Arguments:
            entity: entity to copy images to
        """
        path = os.path.join(self.base_path, entity.path)

        for name in entity.images:
            image = self.site.images[name]
            output = os.path.join(path, name)
            write(image, output)

    def clean_dir(self):
        """clean the output directory"""
        try:
            shutil.rmtree(self.base_path)
        except OSError:
            pass


class FileSystemFileWrapper(FileWrapper):
    def __init__(self, fqp):
        """Wrap a local file. Store its file object in an instance variable.

        :param fqp: full path to file.
        """
        self._file_object = open(fqp, "rb")

    def read(self):
        """:returns: content of the file"""
        self._file_object.seek(0)
        return self._file_object.read()


def dir_walker(path):
    """
    Use os.walk to walk through directory structure. Exclude directories
    starting with a . and yield file names and the directory name.

    Arguments:
        path: path to walk
    """
    for dir_name, dir_names, file_names in os.walk(path):
        skip = False

        # ignore dictionaries starting with a .
        for name in dir_name.split(os.path.sep):
            if name.startswith("."):
                skip = True

        if skip is True:
            continue

        yield (file_names, dir_name)


def create_path(path):
    """
    Create all directories needed to write an entity.

    :param path: path to create
    """
    if path == "":
        return

    if os.path.exists(path):
        return

    try:
        os.makedirs(path)
    except OSError:
        if OSError.errno == errno.EEXIST:
            pass
        else:
            raise


def write(content, path):
    """
    Write an entity to disk

    Arguments:
        content: content to write
        path: path to write to
    """
    if isinstance(content, FileWrapper):
        with open(path, "wb") as output:
            output.write(content.read())
    else:
        with open(path, "w", encoding="utf-8") as output:
            output.write(content)
