#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from zenbo import url


class ContentObject(object):
    """test object"""
    def __init__(self):
        self.slug = None
        self.meta = {'title': "-This! Is? A#/ Test\&   Slug-"}
        self.path = "foo/bar/"


class ValidURLTest(unittest.TestCase):
    def test_slug(self):
        co = ContentObject()
        slug = "this-is-a-test-slug"
        url._generate_slug(co)
        self.assertEqual(slug, co.slug)
    
    def test_url(self):
        co = ContentObject()
        base = "http://www.domain.tld/"
        final_url = "http://www.domain.tld/foo/bar/"
        url._generate_url(co, base)
        self.assertEqual(final_url, co.url)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
