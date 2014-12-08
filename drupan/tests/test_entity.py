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
        self.entity.meta["date"] = datetime.datetime(2014, 01, 30, 14, 56)
        dt = self.entity.created

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)

    def test_created_no_date(self):
        """should use datetime.now() as created date"""
        self.assertEqual(type(self.entity.created), datetime.datetime)

    def test_created_storage(self):
        """should return foo"""
        self.entity.meta["date"] = datetime.datetime(2014, 01, 30, 14, 56)
        self.entity._created = "foo"
        dt = self.entity.created

        self.assertEqual(dt, "foo")

    def test_updated_generation(self):
        """should return a datetime instance"""
        self.entity.meta["updated"] = datetime.datetime(2014, 01, 30, 14, 56)
        dt = self.entity.updated

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)

    def test_updated_storage(self):
        """should return foo"""
        self.entity.meta["updated"] = datetime.datetime(2014, 01, 30, 14, 56)
        self.entity._updated = "foo"
        dt = self.entity.updated

        self.assertEqual(dt, "foo")

    def test_updated_not_existing(self):
        """should return a datetime instance"""
        self.entity.meta["date"] = datetime.datetime(2014, 01, 30, 14, 56)
        dt = self.entity.updated

        self.assertEqual(type(dt), datetime.datetime)
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 01)
        self.assertEqual(dt.day, 30)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 56)
        self.assertEqual(dt, self.entity._updated)

    def test_get_url_value(self):
        """should return 'foo', 'bar' and 2014"""
        self.entity.meta["date"] = datetime.datetime(2014, 01, 30, 14, 56)
        self.entity.meta["foo"] = "foo"
        self.entity.bar = "bar"

        self.assertEqual(self.entity.get_url_value("%foo"), "foo")
        self.assertEqual(self.entity.get_url_value("%bar"), "bar")
        self.assertEqual(self.entity.get_url_value("%year"), "2014")

    def test_url_meta(self):
        """should return /foo/bar/"""
        self.entity.meta["foo"] = "foo"
        self.entity.bar = "bar"
        self.entity.meta["url"] = "%foo/%bar"

        self.assertEqual(self.entity.url, "/foo/bar/")

    def test_url_config_layout(self):
        """should return /foo/2014/1/"""
        self.entity.meta["foo"] = "foo"
        self.entity.meta["date"] = datetime.datetime(2014, 01, 30, 14, 56)
        self.entity.meta["layout"] = "post"
        self.config.url_scheme["post"] = "/%foo/%year/%month/"

        self.assertEqual(self.entity.url, "/foo/2014/1/")

    def test_path(self):
        """should return foo/bar"""
        self.entity.meta["foo"] = "foo"
        self.entity.meta["bar"] = "bar"
        self.entity.meta["layout"] = "post"

        self.config.url_scheme["post"] = "/%foo/%bar/"
        self.assertEqual(self.entity.path, "foo/bar")

        self.entity._url = None
        self.config.url_scheme["post"] = "/%foo/%bar"
        self.assertEqual(self.entity.path, "foo/bar")

        self.entity._url = None
        self.config.url_scheme["post"] = "%foo/%bar/"
        self.assertEqual(self.entity.path, "foo/bar")

    def test_path_slash(self):
        """should return ''"""
        self.entity.meta["layout"] = "post"
        self.config.url_scheme["post"] = "/"
        self.assertEqual(self.entity.path, "")

    def test_url_no_layout(self):
        """should return None"""
        self.assertEqual(self.entity.url, None)

    def test_path_no_url(self):
        """should return None"""
        self.assertEqual(self.entity.path, None)

    def test_date(self):
        """should return a valid date"""
        self.assertEqual(type(self.entity.date), datetime.datetime)

        self.entity.meta["date"] = datetime.date.today()
        self.assertEqual(type(self.entity.date), datetime.date)

    def test_meta_properties(self):
        """should return title and tags"""
        self.entity.meta["title"] = "foo"
        self.entity.meta["tags"] = ["foo", "bar"]

        self.assertEqual(self.entity.title, "foo")
        self.assertEqual(type(self.entity.tags), list)
