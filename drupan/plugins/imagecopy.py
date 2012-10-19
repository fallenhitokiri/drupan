# -*- coding: utf-8 -*-

"""Copy images in the same directory as the post linking to it
options:
  - imagecopy: "path to images"
"""


from HTMLParser import HTMLParser
# TODO: Python 3 renames this to html.parser - transition?

from drupan import fshelpers


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
        self.options = site.config.options_for_key('imagecopy')
        self.output = site.config.output
        self.site = site

        if self.options:
            self.input = site.path + self.options
        else:
            self.input = self.site.config.input + "images/"

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
                fshelpers.copyfile(self.input, img, odir)
