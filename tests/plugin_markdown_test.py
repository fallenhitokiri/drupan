# -*- coding: utf-8 -*-
import unittest
import os
import sys

from .mock import SiteMock

sys.path.insert(0, os.path.abspath('..'))
from drupan.plugins.markdown import Plugin


class MarkdownTestCase(unittest.TestCase):
    """test markdown generation"""
    def test_markdown_generation(self):
        """should run markdown on content"""
        site = SiteMock()
        plugin = Plugin(site)
        plugin.run()

        self.assertEqual(site.entities[0].content, "<p>foobar</p>\n")

    def test_misconfigured(self):
        """should raise an exception"""
        self.assertRaises(Exception, Plugin)
