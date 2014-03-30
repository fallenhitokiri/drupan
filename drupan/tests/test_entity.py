# -*- coding: utf-8 -*-
import unittest
import datetime

from drupan.config import Config
from drupan.entity import Entity


class TestEntity(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.entity = Entity(self.config)

    def test_slug_generation(self):
        """should return a valid slug"""
        expected = "foo-bar"
        title = "-FoO--BaR---"
        self.entity.meta["title"] = title

        self.assertEqual(self.entity.slug, expected)

    def test_slug_storage(self):
        """should return foo, not bar"""
        title = "-FoO--BaR---"
        self.entity.meta["title"] = title
        self.entity._slug = "baz"

        self.assertEqual(self.entity.slug, "baz")

    def test_created_generation(self):
        """should return a datetime instance"""
        self.entity.meta["date"] = "2014-01-30 14:56"
        dt = self.entity.created

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)

    def test_created_storage(self):
        """should return foo"""
        self.entity.meta["date"] = "2014-01-30 14:56"
        self.entity._created = "foo"
        dt = self.entity.created

        self.assertEqual(dt, "foo")

    def test_updated_generation(self):
        """should return a datetime instance"""
        self.entity.meta["updated"] = "2014-01-30 14:56"
        dt = self.entity.updated

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)

    def test_updated_storage(self):
        """should return foo"""
        self.entity.meta["updated"] = "2014-01-30 14:56"
        self.entity._updated = "foo"
        dt = self.entity.updated

        self.assertEqual(dt, "foo")

    def test_updated_not_existing(self):
        """should return a datetime instance"""
        self.entity.meta["date"] = "2014-01-30 14:56"
        dt = self.entity.updated

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)
        self.assertEqual(dt, self.entity._updated)
