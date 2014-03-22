# -*- coding: utf-8 -*-
import unittest

from drupan.config import Config
from drupan.site import Site
from drupan.plugins.tags import Plugin
from drupan.entity import Entity


class TestTests(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.site = Site()
        self.plugin = Plugin(self.site, self.config)

    def test_create_entity(self):
        """should create an entity"""
        self.plugin.create_entity("foO")
        self.assertTrue("foo" in self.plugin.tags)

    def test_generate_tags(self):
        """should create two tags"""
        entity = Entity(self.config)
        entity.meta["tags"] = ["foo", "bar"]

        self.plugin.generate_tags(entity)

        self.assertTrue("foo" in self.plugin.tags)
        self.assertTrue("bar" in self.plugin.tags)

    def test_generate_tags_two_entities(self):
        """should create one tag with two entities"""
        entity1 = Entity(self.config)
        entity1.meta["tags"] = ["foo"]
        entity2 = Entity(self.config)
        entity2.meta["tags"] = ["foo"]

        self.plugin.generate_tags(entity1)
        self.plugin.generate_tags(entity2)

        self.assertEqual(len(self.plugin.tags["foo"].entities), 2)

    def test_generate_tags_no_tags(self):
        """should not raise a KeyError"""
        entity = Entity(self.config)
        self.plugin.generate_tags(entity)

    def test_run(self):
        """should create two entities and add it to the sites entities"""
        entity1 = Entity(self.config)
        entity1.meta["tags"] = ["foo"]
        entity2 = Entity(self.config)
        entity2.meta["tags"] = ["bar"]

        self.site.entities.append(entity1)
        self.site.entities.append(entity2)

        plugin = Plugin(self.site, self.config)
        plugin.run()

        self.assertEqual(len(self.site.entities), 4)
