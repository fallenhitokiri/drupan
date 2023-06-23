# -*- coding: utf-8 -*-
from html.parser import HTMLParser


class ImageParser(HTMLParser):
    """Handler based on HTMLParser for images"""

    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []
        self.exclude = ("/", "//", "https://", "http://", "ftp://")

    def handle_starttag(self, tag, attrs):
        """if image tag is found add it to self.images"""
        if tag == 'img':
            img = dict(attrs)['src']
            # print(f"Found an image {img}")

            if not img.startswith(self.exclude):
                # print("adding")
                self.images.append(img)
            else:
                # print(f"Not adding {img} beacuase starts with {self.exclude}")
                pass
