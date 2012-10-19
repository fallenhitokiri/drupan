# -*- coding: utf-8 -*-

"""
Search links in all content objects and check if all files
were generated.
"""
from HTMLParser import HTMLParser
import os
import sys


class LinkParser(HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append((dict(attrs)['href']))


class Feature(object):
    def __init__(self, site):
        self.url = site.config['url']
        self.output = site.path + site.config['output']['directory']
        self.site = site

    def finalize(self):
        for co in self.site.content:
            if co.markup is not None:
                parser = LinkParser()
                parser.feed(co.markup)

                for link in parser.links:
                    if link[:1] == "/":
                        link_path = self.output + link
                        if not (os.path.exists(link_path)):
                            sys.exit(link_path)
