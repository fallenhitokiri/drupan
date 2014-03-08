# -*- coding: utf-8 -*-
import unittest
import os
import sys

from .mock import SiteMock

sys.path.insert(0, os.path.abspath('..'))
from drupan.plugins.blank import Plugin


class BlankTestCase(unittest.TestCase):
    """test empty entry generation"""
    def test_entity_generation(self):
        """should generate two entities"""
        site = SiteMock()
        site.entities = []  # reset entities

        plugin = Plugin(site)
        plugin.run()

        self.assertEqual(len(site.entities), 2)

    def test_misconfigured(self):
        """should raise an exception"""
        self.assertRaises(Exception, Plugin)
