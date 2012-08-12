# -*- coding: utf-8 -*-

"""
Search in all ContentObjects for images and copy them in them
corresponding directory

configuration:
  - add directory that holds images to your configuration
"""

from HTMLParser import HTMLParser
import shutil
import os
# TODO: Python 3 renames this to html.parser - transition?


class ImageParser(HTMLParser):
    def __init__(self):
        self.images = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.images.append((dict(attrs)["src"]))


class Finalizer(object):
    def __init__(self, site):
        self.input = site.path + site.config['imagecopy']['directory']
        self.output = site.path + site.config['output']['directory']

        if self.input[-1:] is not os.sep:
            self.input = self.input + os.sep

        if self.output[-1:] is not os.sep:
            self.output = self.output + os.sep

        self.site = site

    def finalize(self):
        for co in self.site.content:
            co.images = []

            if co.markup is not None:
                parser = ImageParser()
                parser.feed(co.markup)
                co.images = parser.images

            odir = self.output + co.path

            for img in co.images:
                imgfile = self.input + img
                shutil.copy(imgfile, odir)
