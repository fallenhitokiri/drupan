#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from drupan.core import Drupan


class ValidFullTest(unittest.TestCase):
    def setUp(self):
        self.engine = Drupan()
        path = "tests/example"
        nodeploy = True
        serve = False
        self.engine.setup(path, nodeploy, serve)
        self.engine.run()
    
    def test_size(self):
        self.assertEqual(len(self.engine.site.content), 7)
    
    def test_exist(self):
        post = False
        page = False
        rss = False
        index = False
        tag1 = False
        tag2 = False
        archive = False

        for cobj in self.engine.site.content:
            if cobj.meta['title'] == "title post":
                post = True
                self.post = cobj
            if cobj.meta['title'] == "title page":
                page = True
                self.page = cobj
            if cobj.meta['title'] == "RSS Feed":
                rss = True
                self.rss = cobj
            if cobj.meta['title'] == "Index":
                index = True
                self.index = cobj
            if cobj.meta['title'] == "tag1":
                tag1 = True
                self.tag1 = cobj
            if cobj.meta['title'] == "tag2":
                tag2 = True
                self.tag2 = cobj
            if cobj.meta['title'] == "Archive":
                archive = True
                self.archive = cobj
        
        self.assertTrue(post)
        self.assertTrue(page)
        self.assertTrue(rss)
        self.assertTrue(index)
        self.assertTrue(tag1)
        self.assertTrue(tag2)
        self.assertTrue(archive)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
