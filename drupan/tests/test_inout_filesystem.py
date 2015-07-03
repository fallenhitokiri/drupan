# -*- coding: utf-8 -*-
import unittest

from drupan.config import Config
from drupan.site import Site
from drupan.inout.filesystem import Reader


class TestReader(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.reader = "filesystem"
        self.config.options = {
            "reader": {
                "content": "foo",
                "extension": "md",
                "template": "bar",
            }
        }

        self.site = Site()

    def test_parse_file(self):
        """should add an entity to site.entities"""
        reader = Reader(self.site, self.config)

        # test input - meta["foo"] = "bar" and raw = "baz"
        raw = """
        foo: bar
        ---
        baz"""

        reader.parse_file(raw)
        entity = self.site.entities[0]

        self.assertEqual(entity.meta["foo"], "bar")
        self.assertEqual(entity.raw, "baz")

    def test_init(self):
        """should add a dot before the extension"""
        reader = Reader(self.site, self.config)
        self.assertEqual(reader.extension, ".md")
