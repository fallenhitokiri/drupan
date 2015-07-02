# -*- coding: utf-8 -*-
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class ImageParser(HTMLParser):
    """Handler based on HTMLParser for images"""
    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []

    def handle_starttag(self, tag, attrs):
        """if image tag is found add it to self.images"""
        if tag == 'img':
            self.images.append((dict(attrs)['src']))