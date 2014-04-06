# -*- coding: utf-8 -*-
import unittest

from drupan.site import Site, search
from drupan.entity import Entity


class TestSite(unittest.TestCase):
    def setUp(self):
        self.e1 = Entity({})
        self.e1.meta["title"] = "foo"
        self.e1.meta["layout"] = "post"

        self.e2 = Entity({})
        self.e2.meta["title"] = "bar"
        self.e2.meta["layout"] = "post"
        self.e2.tag = "asdf"

        self.site = Site()
        self.site.entities.append(self.e1)
        self.site.entities.append(self.e2)

    def test_get_title(self):
        """should return e1"""
        entity = self.site.get("title", "foo")
        self.assertEqual(entity, self.e1)

    def test_get_layout(self):
        """should return two entities"""
        results = self.site.get("layout", "post")
        self.assertEqual(len(results), 2)

    def test_get_none(self):
        """should return None"""
        result = self.site.get("foo", "bar")
        self.assertEqual(result, None)

    def test_search_meta(self):
        """should return True"""
        result = search(self.e1, "title", "foo")
        self.assertTrue(result)

    def test_search_attribute(self):
        """should return True"""
        result = search(self.e2, "tag", "asdf")
        self.assertTrue(result)

    def test_search_noresult(self):
        """should return False"""
        result = search(self.e1, "foo", "baz")
        self.assertFalse(result)
