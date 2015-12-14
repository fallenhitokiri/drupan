# -*- coding: utf-8 -*-
import unittest
import os
import sys

from drupan.engine import Engine
from drupan.plugins.blank import Plugin as BlankPlugin


class PluginTests(unittest.TestCase):
    def test_import_base_plugin(self):
        """import blank plugin"""
        engine = Engine()
        engine.config.plugins = ["blank"]
        engine.config.options = {
            "blank": {
                "generate": {
                    "foo": "bar",
                    "baz": "wusa"
                }
            }
        }
        blank = BlankPlugin(engine.site, engine.config)

        engine.prepare_engine()
        self.assertEqual(len(engine.plugins), 1)
        self.assertEqual(engine.plugins[0].__class__, blank.__class__)

    def test_import_third_party_plugin(self):
        """import foo plugin"""
        engine = Engine()
        engine.config.plugins = ["foo"]

        module_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "module",
        )
        sys.path.append(module_path)

        engine.prepare_engine()
        self.assertEqual(len(engine.plugins), 1)
        self.assertFalse(engine.plugins[0].ran)
        self.assertEqual(engine.plugins[0].name, "TestPlugin")
