# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import shutil
import os
# TODO: Python 3 renames this to html.parser - transition?


class ImageParser(HTMLParser):
    """Handler based on HTMLParser for images"""
    def __init__(self):
        self.images = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """if image tag is found add it to self.images"""
        if tag == 'img':
            self.images.append((dict(attrs)['src']))


class Feature(object):
    """Search in all ContentObjects for images and copy them in them
    corresponding directory
    """
    def __init__(self, site):
        self.input = site.path + site.config.options_for_key('imagecopy')
        self.output = site.config.output
        self.site = site

        if self.input[-1:] is not os.sep:
            self.input = self.input + os.sep

    def run(self):
        """run the plugin"""
        for cobj in self.site.content:
            cobj.images = []

            if cobj.markup is not None:
                parser = ImageParser()
                parser.feed(cobj.markup)
                cobj.images = parser.images

            odir = self.output + cobj.path

            for img in cobj.images:
                imgfile = self.input + img
                shutil.copy(imgfile, odir)
