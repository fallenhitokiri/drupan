# -*- coding: utf-8 -*-
import unittest
import os
import sys

import yaml

sys.path.insert(0, os.path.abspath('..'))
from drupan.config import Config


class ConfigTestCase(unittest.TestCase):
    def test_parse_yaml(self):
        """should set attributes for a yaml source"""
        test_dict = {
            "input": "foo",
            "output": "bar",
            "extras": ["foo", "bar"],
            "foo": {
                "baz": 1,
                "bar": 2
            }
        }

        raw = yaml.dump(test_dict)

        config = Config("")
        config.raw = raw
        config.parse_yaml()

        # check attributes
        self.assertTrue(hasattr(config, "input"))
        self.assertTrue(hasattr(config, "output"))
        self.assertTrue(hasattr(config, "extras"))
        self.assertTrue(hasattr(config, "foo"))

        # check values
        self.assertEqual(config.input, "foo")
        self.assertEqual(config.output, "bar")
        self.assertEqual(config.extras[0], "foo")
        self.assertEqual(config.extras[1], "bar")
        self.assertEqual(config.foo["baz"], 1)
        self.assertEqual(config.foo["bar"], 2)

    def test_parse_config(self):
        """should raise an exception"""
        options = {"format": "asdf"}

        config = Config(options)

        self.assertRaises(Exception, config.parse_config)

    def test_get(self):
        """should return a key and raise an exception"""
        cfg = Config("")
        self.assertEqual(cfg.get("raw"), None)
        self.assertRaises(Exception, cfg.get)
