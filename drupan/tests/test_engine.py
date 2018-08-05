# -*- coding: utf-8 -*-
import unittest
import os
import sys

from drupan.engine import Engine
from drupan.plugins.blank import Plugin as BlankPlugin


class MockPlugin(object):
    def __init__(self):
        self.ran = False

    def run(self):
        self.ran = True


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

    def test_external_plugin_path(self):
        """add external_plugins path to Python path so the module imports"""
        engine = Engine()
        engine.config.plugins = ["foo"]
        engine.config.external_plugins = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "module",
        )
        engine.prepare_engine()

        self.assertEqual(len(engine.plugins), 1)
        self.assertFalse(engine.plugins[0].ran)
        self.assertEqual(engine.plugins[0].name, "TestPlugin")

    def add_external_plugins_invalid_path(self):
        """raise an exception if the path does not exist"""
        engine = Engine()
        engine.config.external_plugins = "fj30e32f"
        self.assertRaises(Exception, engine.prepare_engine)

    def test_prepare_engine(self):
        """should load all plugins"""
        engine = Engine()
        engine.config.reader = "filesystem"
        engine.config.writer = "filesystem"
        engine.config.deployment = "gitsub"
        engine.config.options = {
            "reader": {
                "content": "foo",
                "extension": "md",
                "template": "foo",
            },
            "writer": {
                "directory": "foo",
            },
            "gitsub": {
                "path": "foo",
            },
        }
        engine.prepare_engine()

        self.assertIsNotNone(engine.reader)
        self.assertIsNotNone(engine.writer)
        self.assertIsNotNone(engine.deployment)

    def test_run(self):
        """should run all plugins"""
        reader = MockPlugin()
        writer = MockPlugin()
        plugin = MockPlugin()
        renderer = MockPlugin()
        deploy = MockPlugin()

        engine = Engine()
        engine.reader = reader
        engine.writer = writer
        engine.plugins.append(plugin)
        engine.renderer = renderer
        engine.deployment = deploy
        engine.run()

        self.assertTrue(reader.ran)
        self.assertTrue(writer.ran)
        self.assertTrue(plugin.ran)
        self.assertTrue(renderer.ran)
        self.assertTrue(deploy.ran)
