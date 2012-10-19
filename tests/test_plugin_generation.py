#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from drupan.plugins import blank


class Config(object):
    def __init__(self):
        self.url = "http://foo.tld/"
        self.layouts = {
            'index': ["", "_index.html"]
        }

    def options_for_key(self, key):
        opt = {
            'index': ['Index', 'False']
        }
        return opt


class So(object):
    """small site object"""
    def __init__(self):
        cfg = Config()
        self.content = []
        self.config = cfg


class ValidGenerationTest(unittest.TestCase):
    def test_generation(self):
        site = So()
        plugin = blank.Feature(site)
        plugin.run()
        title = site.content[0].meta['title']
        layout = site.content[0].meta['layout']
        menu = site.content[0].menu
        self.assertEqual(title, 'Index')
        self.assertEqual(layout, 'index')
        self.assertEqual(menu, 'False')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
