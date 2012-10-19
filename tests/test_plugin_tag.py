#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from drupan.plugins import tags


class Obj(object):
    """small content object"""
    def __init__(self):
        self.meta = {
            'tags': ['tag1', 'tag2']
        }


class Config(object):
    def __init__(self):
        self.url = "http://foo.tld/"
        self.layouts = {
            'tags': ["tag/$title/", "_tag.html"]
        }


class So(object):
    """small site object"""
    def __init__(self):
        co = Obj()
        self.content = [co]
        cfg = Config()
        self.config = cfg


class ValidTagTest(unittest.TestCase):
    def test_tag_generation(self):
        site = So()
        plugin = tags.Feature(site)
        plugin.run()
        self.assertTrue("tag1" in plugin.tags)
        self.assertTrue("tag2" in plugin.tags)
        self.assertEqual(site.content[1].url, "http://foo.tld/tag/tag1/")
        self.assertEqual(site.content[2].url, "http://foo.tld/tag/tag2/")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
