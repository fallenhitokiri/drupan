# -*- coding: utf-8 -*-
import unittest

from drupan.imageparser import ImageParser


class TestImageParser(unittest.TestCase):
    def test_parsing(self):
        parser = ImageParser()
        parser.feed('<p><img src="foo.jpg" /></p>')

        self.assertEqual(len(parser.images), 1)
        self.assertEqual(parser.images[0], "foo.jpg")

    def test_parsing_skip_with_scheme(self):
        """should only add images that do not start with an path"""
        test_urls = [
            '<p><img src="/bar/foo.jpg" /></p>',
            '<p><img src="/foo.jpg" /></p>',
            '<p><img src="https://foo.jpg" /></p>',
            '<p><img src="http://foo.jpg" /></p>',
            '<p><img src="ftp://foo.jpg" /></p>',
            '<p><img src="//foo.jpg" /></p>'
        ]

        for url in test_urls:
            parser = ImageParser()
            parser.feed(url)
            self.assertEqual(len(parser.images), 0)
