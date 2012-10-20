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

        for cobj in self.engine.site.content:
            if cobj.meta['title'] == "title post":
                self.post = cobj
            if cobj.meta['title'] == "title page":
                self.page = cobj
            if cobj.meta['title'] == "RSS Feed":
                self.rss = cobj
            if cobj.meta['title'] == "Index":
                self.index = cobj
            if cobj.meta['title'] == "tag1":
                self.tag1 = cobj
            if cobj.meta['title'] == "tag2":
                self.tag2 = cobj
            if cobj.meta['title'] == "Archive":
                self.archive = cobj

    def test_size(self):
        self.assertEqual(len(self.engine.site.content), 7)

    def test_post(self):
        self.assertTrue(self.post.meta['title'], 'title post')
        self.assertTrue(self.post.meta['layout'], 'post')
        self.assertTrue(self.post.meta['date'], '2012-10-19 23:58:22')
        self.assertTrue(self.post.meta['tags'], ['tag1', 'tag2'])
        self.assertTrue(self.post.url, "http://localhost:9000/2012/10/19/title-post/")
        self.assertTrue(self.post.path, "2012/10/19/title-post/")

    def test_page(self):
        self.assertTrue(self.page.meta['title'], 'title page')
        self.assertTrue(self.page.meta['layout'], 'post')
        self.assertTrue(self.page.meta['date'], '2012-10-19 23:57:12')
        self.assertTrue(self.page.url, "http://localhost:9000/title-page/")
        self.assertTrue(self.page.path, "title-page/")

    def test_index(self):
        self.assertTrue(self.index.meta['title'], 'Index')
        self.assertTrue(self.index.meta['layout'], 'index')
        self.assertTrue(self.index.url, "http://localhost:9000/")

    def test_rss(self):
        self.assertTrue(self.rss.meta['title'], 'RSS-Feed')
        self.assertTrue(self.rss.meta['layout'], 'feed')
        self.assertTrue(self.rss.url, "http://localhost:9000/feed/")

    def test_tag1(self):
        self.assertTrue(self.tag1.meta['title'], 'tag1')
        self.assertTrue(self.tag1.meta['layout'], 'tag')
        self.assertTrue(self.tag1.url, "http://localhost:9000/tag/tag1/")
        self.assertTrue(self.tag1.path, "tag/tag1/")

    def test_tag2(self):
        self.assertTrue(self.tag2.meta['title'], 'tag2')
        self.assertTrue(self.tag2.meta['layout'], 'tag')
        self.assertTrue(self.tag2.url, "http://localhost:9000/tag/tag2/")
        self.assertTrue(self.tag2.path, "tag/tag2/")

    def test_archive(self):
        self.assertTrue(self.post.meta['title'], 'Archive')
        self.assertTrue(self.post.meta['layout'], 'archive')
        self.assertTrue(self.post.url, "http://localhost:9000/archive/")
        self.assertTrue(self.post.path, "archive/")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
