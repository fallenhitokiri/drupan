# -*- coding: utf-8 -*-

"""
Write site to disk

configuration:
  - add "output" directory to your configuration file
"""

import shutil
import os
import errno


class Feature(object):
    def __init__(self, site):
        self.site = site
        self.output = site.config.output
        self.template = site.config.template

    def __cleandir(self):
        try:
            shutil.rmtree(self.output)
        except os.error:
            pass

    def __copytree(self):
        # TODO: obvious, isn't it?
        pattern = shutil.ignore_patterns('_*')
        shutil.copytree(self.template, self.output, ignore=pattern)

    def __mkdir(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                if OSError.errno == errno.EEXIST:
                    # TODO: looks like passing this one is okay
                    pass
                else:
                    raise

    def __write(self, name, content):
        f = open(name, 'w')
        f.write(content.encode('utf-8'))
        f.close()

    def run(self):
        self.__cleandir()
        self.__copytree()

        for co in self.site.content:
            if len(co.path.split('/')) > 1:
                path = "%s/%s" % (self.output, co.path.rsplit('/', 1)[0])
                self.__mkdir(path)

            name = "%s/%s%s" % (self.output, co.path, 'index.html')

            self.__write(name, co.rendered)
