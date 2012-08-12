# -*- coding: utf-8 -*-

"""
generate blank ContentObjects

should be used if you want to add additional sites based on your exissting
obejcts like an index or archive page.

configuration:
  - add 'blank' with all ContentObjects to generate to your configuration
    file. e.x.

    blank:
      index: ["Index", False]
      archive: ["Archive", True]

    second option specifies if it should be added to your menu
"""

from ..contentobject import ContentObject


class Generator(object):
    def __init__(self, site):
        self.blanks = site.config['blank']
        self.site = site

    def generate(self):
        for current in self.blanks:
            co = ContentObject()
            title = self.blanks[current][0]
            menu = self.blanks[current][1]
            co.add_meta(title, current, menu)
            self.site.content.append(co)
