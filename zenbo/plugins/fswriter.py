# -*- coding: utf-8 -*-

import shutil
import os
import errno


class Feature(object):
    """write site to hd"""
    def __init__(self, site):
        self.site = site
        self.output = site.config.output
        self.template = site.config.template

    def __cleandir(self):
        """remove output directory"""
        try:
            shutil.rmtree(self.output)
        except os.error:
            pass

    def __copytree(self):
        """copy template dir to output dir, ignore '_' files"""
        # TODO: obvious, isn't it?
        pattern = shutil.ignore_patterns('_*')
        shutil.copytree(self.template, self.output, ignore=pattern)

    def __mkdir(self, path):
        """make dir if it does not exist"""
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                if OSError.errno == errno.EEXIST:
                    # looks like passing this one is okay
                    pass
                else:
                    raise

    def __write(self, name, content):
        """write file"""
        with open(name, 'w') as output:
            output.write(content.encode('utf-8'))

    def run(self):
        """run the plugin"""
        self.__cleandir()
        self.__copytree()

        for cobj in self.site.content:
            if len(cobj.path.split('/')) > 1:
                path = "%s/%s" % (self.output, cobj.path.rsplit('/', 1)[0])
                self.__mkdir(path)

            name = "%s/%s%s" % (self.output, cobj.path, 'index.html')

            self.__write(name, cobj.rendered)
