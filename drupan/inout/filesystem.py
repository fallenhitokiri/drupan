# -*- coding: utf-8 -*-
import os
import io


class Reader(object):
    def __init__(self, config):
        """
        Initialize a new filesystem reader

        Arguments:
            config: configuration object
        """
        self.config = config.get("reader_config")
        self.dir = config["dir"]
        self.extension = config.get("extension", ".md")
        self.encoding = config.get("encoding", "utf-8")
        self.files = []

    def get(self):
        """
        Read all input files and return them as list

        Returns:
            list with all input files
        """
        for name in os.listdir(self.dir):
            if self.wrong_extension(name):
                continue

            self.read_file(name)

        return self.files

    def wrong_extension(self, name):
        """
        Check if a filename ends with the configured extension.
        Only do the check if self.extension is not None

        Arguments:
            name: filename

        Returns:
            If the extension matches the end of name
        """
        if self.extension is None:
            return False

        if name.endswith(self.extension):
            return False

        return True

    def read_file(self, name):
        """
        Read a file and append its content to self.files

        Arguments:
            name: filename
        """
        inp = os.path.join(self.dir, name)

        with io.open(inp, "r", encoding=self.encoding) as source:
            read = source.read()
            self.files.append(read)
