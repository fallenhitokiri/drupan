# -*- coding: utf-8 -*-
import unittest

from drupan.imageparser import ImageParser


class TestImageParser(unittest.TestCase):
    def test_parsing(self):
        parser = ImageParser()
        parser.feed('<p><img src="foo.jpg" /></p>')

        self.assertEqual(len(parser.images), 1)
        self.assertEqual(parser.images[0], "foo.jpg")