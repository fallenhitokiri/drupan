# -*- coding: utf-8 -*-

from drupan import fshelpers


class Feature(object):
    """write site to hd"""
    def __init__(self, site):
        self.site = site
        self.output = site.config.output
        self.template = site.config.template

    def run(self):
        """run the plugin"""
        fshelpers.cleandir(self.output)
        fshelpers.copytree(self.template, self.output)

        for cobj in self.site.content:
            if len(cobj.path.split('/')) > 1:
                path = "%s/%s" % (self.output, cobj.path.rsplit('/', 1)[0])
                fshelpers.mkdir(path)

            name = "%s/%s%s" % (self.output, cobj.path, 'index.html')

            fshelpers.write(name, cobj.rendered)
