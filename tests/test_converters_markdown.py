#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from zenbo.plugins import markdown


def comp(co):
    if co.markup == "<p>foo</p>\n":
        return True
    else:
        return False


class Obj(object):
    """small content object"""
    def __init__(self):
        self.content = "foo"
        self.markup = None


class So(object):
    """small site object"""
    def __init__(self):
        co = Obj()
        self.content = [co]


class ValidMarkdownTest(unittest.TestCase):
    def test_markup(self):
        site = So()
        plugin = markdown.Feature(site)
        plugin.run()
        self.failUnless(comp(site.content[0]))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
