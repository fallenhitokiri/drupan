# -*- coding: utf-8 -*-
import unittest

from drupan.config import Config
from drupan.site import Site
from drupan.plugins.blank import Plugin


class TestBlank(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.options = {
            "blank": {
                "generate": {
                    "foo": "bar",
                    "baz": "wusa"
                }
            }
        }

        self.site = Site()

    def test_run(self):
        """should generate two entities"""
        plugin = Plugin(self.site, self.config)
        plugin.run()

        self.assertEqual(len(self.site.entities), 2)

    def test_init_list(self):
        """should convert the list to a dictionary"""
        self.config.options["blank"]["generate"] = ["foo", "bar"]
        plugin = Plugin(self.site, self.config)

        self.assertEqual(plugin.generate["foo"], "foo")
        self.assertEqual(plugin.generate["bar"], "bar")
