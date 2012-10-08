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
from ..url import prepare


class Feature(object):
    def __init__(self, site):
        self.site = site
        self.options = site.config.options_for_key("blank")

    def run(self):
        for current in self.options:
            co = ContentObject()
            title = self.options[current][0]
            menu = self.options[current][1]
            co.add_meta(title, current, menu)
            prepare(co, self.site)
            self.site.content.append(co)
