# -*- coding: utf-8 -*-
import os
import unittest

from drupan.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.yaml = """
        reader: bar
        plugins: ["1", "2", "3"]
        """

        self.cfg = {
            "reader": "bar",
            "plugins": ["1", "2", "3"]
        }

        self.options = {
            "reader": {
                "directory": "foobar",
            },
            "markdown": {
                "plugins": [1, 2, 3],
                "highlight": True
            }
        }

        self.config = Config()

    def test_parse_yaml(self):
        """should have a reader and plugins set"""
        self.config.parse_yaml(self.yaml)
        self.assertEqual(self.config.reader, "bar")
        self.assertEqual(len(self.config.plugins), 3)

    def test_config_from_drict(self):
        """should have a reader and plugins set"""
        self.config.from_dict(self.cfg)
        self.assertEqual(self.config.reader, "bar")
        self.assertEqual(len(self.config.plugins), 3)

    def test_get_options(self):
        """should return valid options"""
        self.config.options = self.options
        self.assertEqual(
            self.config.get_option("reader", "directory"),
            "foobar"
        )
        self.assertEqual(len(self.config.get_option("markdown", "plugins")), 3)
        self.assertTrue(self.config.get_option("markdown", "highlight"))

    def test_get_options_exception(self):
        """should raise an exception"""
        self.assertRaises(Exception, self.config.get_option)

    def test_get_option_redirects(self):
        """should return a dictionary for a root element"""
        self.config.redirects = {"foo": "bar"}
        redirects = self.config.get_option(None, "redirects")
        self.assertEqual(type(redirects), dict)

    def test_env_loader(self):
        os.environ["drupan_test_foo"] = "bar"

        yaml = """options:
          bar:
            foo: <%= ENV['drupan_test_foo'] %>
        """
        self.config.parse_yaml(yaml)

        del os.environ["drupan_test_foo"]

        self.assertEqual(self.config.get_option("bar", "foo"), "bar")


if __name__ == "__main__":
    unittest.main()
